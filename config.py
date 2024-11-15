class Config:
    # Base config
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
