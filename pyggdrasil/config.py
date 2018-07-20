class Config:
    SECRET_KEY = "You will never know"
    MONGO_URI = "mongodb://localhost:27017/pyggdrasil"
    REDIS_URL = "redis://localhost:6379/0"


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    pass


class ProdConfig(Config):
    pass


config_by_name = dict(
    dev=DevConfig,
    test=TestConfig,
    prod=ProdConfig
)
