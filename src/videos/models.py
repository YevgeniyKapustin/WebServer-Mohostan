from sqlalchemy import Column, String

from src.database import Base


class Video(Base):
    title: str = Column(String(), nullable=False)
    path: str = Column(String(), nullable=False)
