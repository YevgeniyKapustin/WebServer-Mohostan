from sqlalchemy import Column, Integer, ForeignKey, TEXT, String

from src.database import Base


class Command(Base):
    id = Column(Integer, primary_key=True)
    type = Column(String(), nullable=False)
    request = Column(TEXT, nullable=False)
    response = Column(TEXT, nullable=False)
