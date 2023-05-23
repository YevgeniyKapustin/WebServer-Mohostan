from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from src.database import Base


class Type(Base):
    __tablename__ = 'type'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(50), nullable=False, unique=True)

    command = relationship(
        'Command',
        backref='types',
        cascade='all, delete, delete-orphan'
    )
