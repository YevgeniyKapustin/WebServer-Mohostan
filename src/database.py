"""Сбор метаданных и создание сессии"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import POSTGRES_URL

Base = declarative_base()

engine = create_engine(POSTGRES_URL)
session = sessionmaker(bind=engine)()
