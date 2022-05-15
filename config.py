import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    SERVER_NAME = "127.0.0.1:5000"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI")
