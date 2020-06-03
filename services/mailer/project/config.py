
class BaseConfig:
    TESTING = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

class DevelopmentConfig(BaseConfig):
    MAIL_USERNAME = "mltestplatform@gmail.com"
    MAIL_PASSWORD = "UQPxLXR$R@Lm"
    MAIL_DEBUG = True

class TestingConfig(BaseConfig):
    TESTING = True

class ProductionConfig(BaseConfig):
    pass
