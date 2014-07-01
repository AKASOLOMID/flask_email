
class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'db/email_flask.db'

class ProductionConfig(Config):
    DATABASE_URI = 'db/email_flask.db'



class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'sqlite://:memory:'
class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = 'test/test.db'
