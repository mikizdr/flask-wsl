import os
from typing import Union

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    TESTING = False
    ENV = "development"


class ProductionConfig(Config):
    DATABASE_URI = "mysql://user@localhost/test"


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI: Union[str, None] = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///app_database.db"
    )
    SECRET_KEY: Union[str, None] = os.getenv(
        "APP_SECRET_KEY", "change_me_if_there_is_no_dotenv_file_or_create_dotenv_file"
    )


class TestingConfig(Config):
    DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
