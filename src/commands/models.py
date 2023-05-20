from sqlalchemy import Column, Integer, ForeignKey, TEXT
from sqlalchemy.orm import relationship

from src.database import Base


class Command(Base):
    __tablename__ = 'command'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('type.id'), nullable=False)
    request = Column(TEXT, nullable=False)
    response = Column(TEXT, nullable=False)

    type = relationship('Type', backref='commands')
