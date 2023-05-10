from sqlalchemy import Column, String, Integer

from src.database import Base


class Type(Base):
    __tablename__ = 'type'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(50), nullable=False, unique=True)
