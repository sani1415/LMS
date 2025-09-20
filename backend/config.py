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
    """Development configuration for local testing"""
    DEBUG = True
    # Using SQLite for simple local development to avoid database setup.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///library_dev.db'

class ProductionConfig(Config):
    """Production configuration for cPanel deployment"""
    DEBUG = False
    
    # --- THIS SECTION IS NOW CORRECTED ---
    # It builds the database connection string from the variables you set in cPanel.
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    
    # Construct the database URI only if all parts are present
    if all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        )
    else:
        # This will give a clear error if a variable is missing in cPanel
        raise ValueError("One or more database environment variables are not set in cPanel.")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary that the application will use
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}