from sqlalchemy import Column, String

from src.database import Base


class User(Base):
    email: str = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String(length=1024), nullable=False)
