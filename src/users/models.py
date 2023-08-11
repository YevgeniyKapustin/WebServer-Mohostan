from sqlalchemy import Column, Integer, String, Boolean

from src.database import Base


class User(Base):
    email: str = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String(length=1024), nullable=False)
