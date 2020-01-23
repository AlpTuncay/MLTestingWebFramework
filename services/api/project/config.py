

class BaseConfig:
    TESTING = False
    DEBUG = False
    SECRET_KEY = "secret"


class DevelopmentConfig(BaseConfig):
    TESTING = False
    DEBUG = True
    FLASK_ENV = "development"


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    FLASK_ENV = "production"


