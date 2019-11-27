

class BaseConfig:
    TESTING = False
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    TESTING = False
    DEBUG = True
    FLASK_ENV = "development"
    PRESERVE_CONTEXT_ON_EXCEPTION = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    FLASK_ENV = "production"


