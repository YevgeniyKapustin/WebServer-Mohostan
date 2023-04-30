from dotenv import load_dotenv
from os import environ

load_dotenv()

DB_USER: str = environ.get('DB_USER')
DB_PASS: str = environ.get('DB_PASS')
DB_HOST: str = environ.get('DB_HOST')
DB_PORT: str = environ.get('DB_PORT')
DB_NAME: str = environ.get('DB_NAME')
DB_URL: str = (
    f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)
