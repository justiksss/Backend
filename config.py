from dotenv import load_dotenv

import os

load_dotenv()

DB_PASS = os.environ.get("DB_PASS")
DB_USER = os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")
DB_HOST = os.environ.get("DB_HOST")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


db_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"



