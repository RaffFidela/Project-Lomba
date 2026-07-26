import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    DATABASE = os.environ.get('DATABASE', os.path.join(os.getcwd(), 'sarpras.db'))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    
config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)
