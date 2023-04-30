from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import DB_URL

Base = declarative_base()

engine = create_engine(DB_URL)
session = sessionmaker(bind=engine)()
