from pydantic import BaseModel

# ✅ Schema for user signup response
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    did: str
    public_key: str
    private_key: str  # User must store this securely

    class Config:
        from_attributes = True

# ✅ Schema for user signup request
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# ✅ Schema for user login request
class UserLogin(BaseModel):
    username: str
    password: str

# ✅ Schema for JWT Token Response
class Token(BaseModel):
    access_token: str
    token_type: str

# ✅ Schema for verifying a signed message
class VerifySignatureRequest(BaseModel):
    username: str
    message: str
    signature: str  # Base64 encoded signature
