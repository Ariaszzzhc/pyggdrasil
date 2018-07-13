class Config:
    SECRET_KEY = "You will never know"


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
