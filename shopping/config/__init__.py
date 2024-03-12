import os
from typing import Union

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    TESTING = False
    ENV = "development"
    PORT = os.getenv("APP_PORT", 5000)
    MAX_PER_PAGE = os.getenv("MAX_PER_PAGE", 10)
    PER_PAGE = os.getenv("PER_PAGE", 5)


class ProductionConfig(Config):
    DATABASE_URI = "mysql://user@localhost/test"
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "storage/uploads")
    ALLOWED_EXTENSIONS: set[str] = os.getenv(
        "ALLOWED_EXTENSIONS", {"png", "jpg", "jpeg", "gif"}
    )


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI: Union[str, None] = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///app_database.db"
    )
    SECRET_KEY: Union[str, None] = os.getenv(
        "APP_SECRET_KEY", "change_me_if_there_is_no_dotenv_file_or_create_dotenv_file"
    )
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "storage/uploads")
    ALLOWED_EXTENSIONS: set[str] = os.getenv(
        "ALLOWED_EXTENSIONS", {"png", "jpg", "jpeg", "gif"}
    )


class TestingConfig(Config):
    DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
