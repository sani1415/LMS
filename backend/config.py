import os

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///library.db'
    
    # Pagination defaults
    BOOKS_PER_PAGE = 100
    LOGS_PER_PAGE = 100
    HISTORY_PER_PAGE = 100

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'

class DevelopmentMySQLConfig(Config):
    """Development configuration with MySQL"""
    DEBUG = True
    # MySQL connection string format: mysql+pymysql://user:password@host:port/database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:@localhost:3306/library'

class ProductionConfig(Config):
    """Production configuration for cPanel deployment"""
    DEBUG = False
    # cPanel MySQL format: mysql+pymysql://username:password@localhost/database_name
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://username:password@localhost/database_name'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'development_mysql': DevelopmentMySQLConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
