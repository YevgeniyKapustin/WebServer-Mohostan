from sqlalchemy import Column, Integer, String, Boolean

from src.database import Base


class User(Base):
    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_trusted: bool = Column(Boolean, default=False, nullable=False)
