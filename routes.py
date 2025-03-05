from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal,get_db
from models import User, Identity
from schemas import UserCreate, UserResponse, UserLogin, VerifySignatureRequest, Token
from passlib.context import CryptContext
from jose import jwt, JWTError
import os
import uuid
import logging
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from base64 import b64decode, b64encode
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Secret key & hashing config
SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecret")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ FastAPI Router
router = APIRouter()

# ✅ Bearer Token Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ✅ Function to hash passwords
def hash_password(password: str):
    return pwd_context.hash(password)

# ✅ Function to verify JWT token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# ✅ Function to generate a unique DID
def generate_did(username: str) -> str:
    """Generate a unique Decentralized Identifier (DID) for a user."""
    unique_id = uuid.uuid4().hex[:12]
    return f"did:identity:{username}-{unique_id}"

# ✅ Function to generate RSA Key Pair
def generate_key_pair():
    """Generate RSA public & private keys for identity verification."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Convert keys to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    return private_pem, public_pem

# ✅ Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Register a new user (Signup)
@router.post("/signup", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password, is_active=True)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user_did = generate_did(user.username)
    private_key, public_key = generate_key_pair()

    new_identity = Identity(user_id=new_user.id, did=user_did, public_key=public_key)
    db.add(new_identity)
    db.commit()
    db.refresh(new_identity)

    logger.info(f"✅ DID & Public Key Created: {user_did}")

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "is_active": new_user.is_active,
        "did": user_did,
        "public_key": public_key,
        "private_key": private_key  # User must store this securely
    }

# ✅ Login User & Generate JWT Token
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # Generate JWT token
    token_data = {"sub": db_user.username}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}

# ✅ Protected Route (JWT Required)
@router.get("/protected")
def protected_route(username: str = Depends(verify_token)):
    return {"message": f"Hello, {username}! You have access to this protected route."}

# ✅ Retrieve a user's DID & Public Key
@router.get("/did")
def get_user_did(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    identity = db.query(Identity).filter(Identity.user_id == user.id).first()
    if not identity:
        raise HTTPException(status_code=404, detail="DID not found")

    return {
        "username": user.username,
        "did": identity.did,
        "public_key": identity.public_key
    }

# ✅ Signature Verification Route
@router.post("/verify")
def verify_signature(request: VerifySignatureRequest, db: Session = Depends(get_db)):
    """Verify a message signature using the stored public key."""
    
    # 🔹 Fetch user identity based on username
    identity = db.query(Identity).join(User).filter(User.username == request.username).first()
    if not identity:
        raise HTTPException(status_code=404, detail="User not found")

    # 🔹 Decode the public key from PEM format
    try:
        public_key = serialization.load_pem_public_key(
            identity.public_key.encode(),
            backend=default_backend()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid public key: {str(e)}")

    # 🔹 Decode the signature from Base64
    try:
        signature_bytes = b64decode(request.signature)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature format")

    # 🔹 Verify the signature
    try:
        public_key.verify(
            signature_bytes,
            request.message.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return {"message": "Signature is valid ✅"}
    except Exception:
        return {"message": "Signature verification failed ❌"}
