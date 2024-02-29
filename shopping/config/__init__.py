class Config(object):
    TESTING = False
    ENV = "development"


class ProductionConfig(Config):
    DATABASE_URI = "mysql://user@localhost/test"


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///shopping.db"
    SECRET_KEY = "yziSWR7ZXM4tLeJJIDjjdtMe18OjO3urIl42tgxnW9w"


class TestingConfig(Config):
    DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
