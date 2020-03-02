

class BaseConfig:
    TESTING = False
    DEBUG = False
    SECRET_KEY = "secret"


class DevelopmentConfig(BaseConfig):
    TESTING = False
    DEBUG = True
    FLASK_ENV = "development"
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    FLASK_ENV = "production"


