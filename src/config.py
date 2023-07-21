class Config:
    SECRET_KEY = 'SOFTWARE_123'

class DevelopmentConfig(Config):
    DEBUG = True
    PGSQL_HOST = 'localhost'
    PGSQL_USER = 'postgres'
    PGSQL_PASSWORD = 'MAguerra2003'
    PGSQL_DATABASE = 'ProyectoSoftware'

config = {
    'development': DevelopmentConfig
}