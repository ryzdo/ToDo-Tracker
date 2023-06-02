import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SECRET_KEY = os.getenv("SECRET_KEY", "")
SQLALCHEMY_TRACK_MODIFICATIONS = False
