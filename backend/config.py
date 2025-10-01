#
# PASTE THIS ENTIRE CODE INTO: backend/config.py
#
import os

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secure-default-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Pagination defaults
    BOOKS_PER_PAGE = 100
    LOGS_PER_PAGE = 100
    HISTORY_PER_PAGE = 100

class DevelopmentConfig(Config):
    """Development configuration - MySQL for consistency"""
    DEBUG = True
    # MySQL configuration for local development - SAME AS PRODUCTION
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root@localhost/library?charset=utf8mb4&collation=utf8mb4_unicode_ci'
    # Connection pool settings to handle connection drops
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0
    }

class ProductionConfig(Config):
    """Production configuration for cPanel deployment"""
    DEBUG = False

    # --- THIS SECTION IS NOW CORRECTED ---
    # It builds the database connection string from the variables you set in cPanel.
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')

    # Construct the database URI - set to None if variables are missing
    # This prevents errors during class definition, error will only occur if this config is actually used
    if all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4&collation=utf8mb4_unicode_ci&connect_timeout=60&read_timeout=60&write_timeout=60&autocommit=true"
    else:
        # Set to None - the application will check this and provide a clear error message
        SQLALCHEMY_DATABASE_URI = None

    # Connection pool settings for cPanel stability - optimized for shared hosting
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 1,  # Conservative pool size for shared hosting
        'pool_timeout': 30,  # Increased timeout for slower connections
        'pool_recycle': 180,  # Shorter recycle time to prevent timeouts
        'pool_pre_ping': True,  # Always verify connections before use
        'max_overflow': 0,  # No overflow connections
        'connect_args': {
            'connect_timeout': 60,
            'read_timeout': 60,
            'write_timeout': 60,
            'autocommit': True,
            'charset': 'utf8mb4',
            'use_unicode': True,
            'sql_mode': 'TRADITIONAL'
        }
    }

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary that the application will use
config = {
    'development': DevelopmentConfig,
    'development_mysql': DevelopmentConfig,  # Same as development
    'development_sqlserver': DevelopmentConfig,  # Same as development
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}