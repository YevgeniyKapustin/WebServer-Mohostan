from sqlalchemy import Column, Integer, TEXT, String

from src.database import Base


class Command(Base):
    type = Column(String(), nullable=False)
    request = Column(TEXT, nullable=False)
    response = Column(TEXT, nullable=False)
