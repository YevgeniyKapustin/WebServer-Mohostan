from sqlalchemy import Column, String, Integer, TEXT, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Type(Base):
    __tablename__ = 'type'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(50), nullable=False, unique=True)


class NormalRequest(Base):  # temporary
    __tablename__ = 'normal_request'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    type_id = Column(Integer, ForeignKey('Type.id'), nullable=False)
    request = Column(TEXT, nullable=False)
    response = Column(TEXT, nullable=False)
    type = relationship('Type')


class ContextualRequest(Base):  # temporary
    __tablename__ = 'contextual_request'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    type_id = Column(Integer, ForeignKey('Type.id'), nullable=False)
    request = Column(TEXT, nullable=False)
    response = Column(TEXT, nullable=False)
    type = relationship('type')
