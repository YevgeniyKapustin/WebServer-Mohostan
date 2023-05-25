from sqlalchemy import Column, Integer, ForeignKey, TEXT

from src.database import Base


class Command(Base):
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('type.id'), nullable=False)
    request = Column(TEXT, nullable=False)
    response = Column(TEXT, nullable=False)
