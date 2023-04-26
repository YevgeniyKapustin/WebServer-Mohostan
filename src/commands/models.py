from sqlalchemy import Column, String, Integer, TEXT, ForeignKey

from database import Base


class Type(Base):
    __tablename__ = 'type'

    id = Column(Integer, primary_key=True)
    type = Column(String)


class NormalRequest(Base):
    __tablename__ = 'normal_request'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('Type.id'), nullable=False)
    request = Column(TEXT, nullable=False)
    response = Column(TEXT, nullable=False)


class ContextualRequest(Base):
    __tablename__ = 'contextual_request'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('Type.id'), nullable=False)
    request = Column(TEXT, nullable=False)
    response = Column(TEXT, nullable=False)
