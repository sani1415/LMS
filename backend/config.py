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

class DevelopmentMySQLConfig(Config):
    """Development configuration with MySQL for local testing"""
    DEBUG = True
    # MySQL configuration for local development
    # Using your existing 'library' database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root@localhost/library'

class DevelopmentSQLServerConfig(Config):
    """Development configuration with SQL Server for local testing"""
    DEBUG = True
    # SQL Server configuration for local development
    # Using your existing 'library' database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mssql+pyodbc://@localhost/library?driver=SQL+Server&trusted_connection=yes'

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
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    else:
        # Set to None - the application will check this and provide a clear error message
        SQLALCHEMY_DATABASE_URI = None

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary that the application will use
config = {
    'development': DevelopmentConfig,
    'development_mysql': DevelopmentMySQLConfig,
    'development_sqlserver': DevelopmentSQLServerConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}