import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = os.getenv("SECRET_KEY")
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
SCHEMA = os.getenv("SCHEMA")

VERSION = "0.0.1"
DEVELOPERS = "Nicola Costa, Vram Rh'em"

SQLALCHEMY_DATABASE_URI  = f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DATABASE}'