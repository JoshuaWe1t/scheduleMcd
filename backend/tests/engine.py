import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Загрузить переменные из .env в окружение
load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
SCHEMA = os.getenv("SCHEMA")

engine = create_engine(url=f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DATABASE}', echo=True)