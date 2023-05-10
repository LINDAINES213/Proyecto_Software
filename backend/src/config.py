class Config:
    SECRET_KEY = 'SOFTWARE_123'

class DevelopmentConfig(Config):
    DEBUG = True
    PGSQL_HOST = 'localhost'
    PGSQL_USER = 'postgres'
    PGSQL_PASSWORD = 'Lind@1155'
    PGSQL_DATABASE = 'proyecto_software'

config = {
    'development': DevelopmentConfig
}