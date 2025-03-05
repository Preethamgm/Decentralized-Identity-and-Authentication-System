from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# ✅ User Model (Stores user credentials)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship to Identity
    identity = relationship("Identity", back_populates="user", uselist=False)

# ✅ Identity Model (Stores Decentralized Identifiers and Public Keys)
class Identity(Base):
    __tablename__ = "identities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    did = Column(String, unique=True, nullable=False)  # Decentralized Identifier
    public_key = Column(String, nullable=False)  # ✅ Store public key for verification

    # Relationship back to User
    user = relationship("User", back_populates="identity")
