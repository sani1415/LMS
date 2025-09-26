#
# PASTE THIS ENTIRE CODE INTO: app.py
#
import os
import sys
import io
import pymysql
from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.config import config
from backend.extensions import db, bcrypt
from backend.models import Book, User, Category, Publisher, Member # Import models
from flask_migrate import Migrate

# Suppress fileno errors in cPanel environment
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Handle fileno operation issues in cPanel
try:
    # Test if fileno operations work
    if hasattr(sys.stdout, 'fileno'):
        sys.stdout.fileno()
        sys.stderr.fileno()
except (AttributeError, io.UnsupportedOperation, OSError):
    # Replace stdout and stderr with safer versions
    class SafeOutput:
        def __init__(self, original):
            self.original = original
        def write(self, x):
            try:
                self.original.write(x)
            except:
                pass
        def flush(self):
            try:
                self.original.flush()
            except:
                pass
        def fileno(self):
            raise io.UnsupportedOperation("fileno not supported")

    sys.stdout = SafeOutput(sys.stdout)
    sys.stderr = SafeOutput(sys.stderr)


# Determine the config name from the environment variable
# Use APP_ENV instead of deprecated FLASK_ENV
config_name = os.environ.get('APP_ENV') or os.environ.get('FLASK_ENV', 'development_mysql')

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config[config_name])

# Check if ProductionConfig is being used but database URI is None
if config_name == 'production' and app.config.get('SQLALCHEMY_DATABASE_URI') is None:
    raise ValueError("Production configuration requires database environment variables (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME) to be set in cPanel.")

# Initialize extensions with the app
db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate
CORS(app)  # Enable CORS for frontend integration

# Add error handlers for database issues
@app.teardown_appcontext
def close_db_session(error):
    """Ensure database sessions are properly closed"""
    if hasattr(db, 'session'):
        try:
            if error:
                db.session.rollback()
        except Exception as e:
            # Ignore "Command Out of Sync" errors during cleanup
            if "Command Out of Sync" not in str(e):
                print(f"Session cleanup error: {e}")
        finally:
            try:
                db.session.remove()
            except:
                pass  # Ignore errors during session removal

@app.errorhandler(Exception)
def handle_database_errors(error):
    """Handle database connection errors gracefully"""
    if 'MySQL server has gone away' in str(error) or 'Broken pipe' in str(error):
        print(f"Database connection error handled: {error}")
        try:
            db.session.rollback()
        except:
            pass
        try:
            db.session.remove()
        except:
            pass
        # Return a generic error response instead of crashing
        return {"error": "Database connection issue, please try again"}, 500
    raise error

def ensure_database_exists():
    """Create database if it doesn't exist"""
    connection = None
    cursor = None
    try:
        if config_name == 'development_mysql':
            # Local development - connect without specifying database
            connection = pymysql.connect(
                host='localhost',
                user='root',
                charset='utf8mb4'
            )
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS library CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            connection.commit()
            print("Local database 'library' ensured to exist")

        elif config_name == 'production':
            # Production cPanel - database should already exist, just verify connection
            db_user = os.environ.get('DB_USER')
            db_password = os.environ.get('DB_PASSWORD')
            db_host = os.environ.get('DB_HOST')
            db_name = os.environ.get('DB_NAME')

            if not all([db_user, db_password, db_host, db_name]):
                raise ValueError("Production requires DB_USER, DB_PASSWORD, DB_HOST, DB_NAME environment variables")

            # Test connection to verify database exists
            connection = pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name,
                charset='utf8mb4'
            )
            print(f"Production database '{db_name}' connection verified")

    except Exception as e:
        print(f"Error with database: {e}")
        # Don't raise exception - let the app continue and let SQLAlchemy handle it
    finally:
        # Safely close connections
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Import and register routes after app and db are initialized to avoid circular imports
from backend.routes import register_routes
from backend.auth_routes import register_auth_routes

# Register all routes
register_routes(app)
register_auth_routes(app)

# --- STATIC FILE SERVING ROUTES ---
@app.route('/')
def serve_main_app():
    """Serve the main Library Management System application"""
    return send_from_directory('.', 'index.html')

@app.route('/favicon.ico')
def favicon():
    return ''

@app.route('/<path:filename>')
def serve_static_files(filename):
    """Serve static files (CSS, JS, images)"""
    # This is a simple way; for high performance, Apache/Nginx should handle this.
    return send_from_directory('.', filename)
# --- END OF STATIC FILE SERVING ---

def create_admin_user():
    """Create default admin user if none exists"""
    try:
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')

        # Check if specific admin user exists (not just any user)
        existing_admin = User.query.filter_by(username=admin_username).first()

        if not existing_admin:
            # Create default admin user
            admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')

            admin = User(username=admin_username, password=admin_password)
            db.session.add(admin)
            db.session.commit()

            print(f"Admin user created: {admin_username}")
            print(f"Admin password: {admin_password}")
            print("IMPORTANT: Change the admin password after first login!")
        else:
            print(f"Admin user '{admin_username}' already exists")

    except Exception as e:
        print(f"Error creating admin user: {e}")
        try:
            db.session.rollback()
        except:
            pass

def create_sample_data():
    """Create sample data for local development only"""
    # Only run this in development mode, never in production
    if app.config.get('DEBUG') is False:
        return

    try:
        # Create sample categories
        if not Category.query.first():
            categories = [
                Category(name='Fiction', description='Fiction books'),
                Category(name='Non-Fiction', description='Non-fiction books'),
                Category(name='Science', description='Science books'),
                Category(name='Technology', description='Technology books')
            ]
            for cat in categories:
                db.session.add(cat)
        
        # Create sample publishers
        if not Publisher.query.first():
            publishers = [
                Publisher(name='Penguin Books', address='London, UK'),
                Publisher(name='Oxford University Press', address='Oxford, UK'),
                Publisher(name='McGraw-Hill', address='New York, USA')
            ]
            for pub in publishers:
                db.session.add(pub)
        
        # Create sample members
        if not Member.query.first():
            members = [
                Member(name='John Doe', email='john@example.com', phone='123-456-7890'),
                Member(name='Jane Smith', email='jane@example.com', phone='098-765-4321')
            ]
            for member in members:
                db.session.add(member)
        
        # Commit the basic data first
        db.session.commit()
        
        # Create sample books (only if no books exist)
        if not Book.query.first():
            fiction_cat = Category.query.filter_by(name='Fiction').first()
            science_cat = Category.query.filter_by(name='Science').first()
            penguin_pub = Publisher.query.filter_by(name='Penguin Books').first()
            
            books = [
                Book(
                    book_name='The Great Gatsby',
                    author='F. Scott Fitzgerald',
                    category_id=fiction_cat.id if fiction_cat else 1,
                    editor='Maxwell Perkins',
                    volumes=1,
                    publisher_id=penguin_pub.id if penguin_pub else 1,
                    year=1925,
                    copies=2,
                    status='Available',
                    completion_status='Complete',
                    note='Classic American novel about the Jazz Age'
                ),
                Book(
                    book_name='To Kill a Mockingbird',
                    author='Harper Lee',
                    category_id=fiction_cat.id if fiction_cat else 1,
                    editor='Tay Hohoff',
                    volumes=1,
                    publisher_id=penguin_pub.id if penguin_pub else 1,
                    year=1960,
                    copies=1,
                    status='Available',
                    completion_status='Complete',
                    note='Pulitzer Prize winner'
                ),
                Book(
                    book_name='Introduction to Physics',
                    author='John Smith',
                    category_id=science_cat.id if science_cat else 2,
                    editor=None,
                    volumes=2,
                    publisher_id=penguin_pub.id if penguin_pub else 1,
                    year=2020,
                    copies=3,
                    status='Available',
                    completion_status='Incomplete',
                    note='Missing volume 2'
                )
            ]
            for book in books:
                db.session.add(book)
        
        db.session.commit()
        print("Sample data created successfully")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.session.rollback()

def initialize_database():
    """Initialize database for both development and production"""
    # Use database marker instead of global flag to persist across restarts
    try:
        with app.app_context():
            # Check if initialization marker exists in database
            result = db.session.execute(db.text("SELECT 1 FROM information_schema.tables WHERE table_name = 'initialization_marker'"))
            if result.fetchone() and config_name == 'production':
                print("Database already initialized (marker found), skipping...")
                return
    except:
        pass  # Database might not be ready yet

    # Ensure database exists/is accessible
    ensure_database_exists()

    with app.app_context():
        if config_name == 'production':
            # Production: Use Flask-Migrate for proper schema management
            try:
                from flask_migrate import upgrade
                upgrade()  # Run any pending migrations
                print("Database migrated successfully using Flask-Migrate")
            except Exception as e:
                print(f"Migration error: {e}")
                # Fallback to create_all if migrations fail
                db.create_all()
                print("Fallback: Database tables created with db.create_all()")
        else:
            # Development: Use simple db.create_all()
            db.create_all()
            print("Development: Database tables created with db.create_all()")

        # Create admin user
        create_admin_user()

        # Add sample data only for development
        if config_name == 'development_mysql' and not Book.query.first():
            print("Database is empty, creating sample data...")
            create_sample_data()
            print("Sample data created.")

        # Create initialization marker for production to prevent re-runs
        if config_name == 'production':
            try:
                db.session.execute(db.text("CREATE TABLE IF NOT EXISTS initialization_marker (id INT PRIMARY KEY DEFAULT 1, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"))
                db.session.execute(db.text("INSERT IGNORE INTO initialization_marker (id) VALUES (1)"))
                db.session.commit()
            except:
                pass

    print("Database initialization completed")

if __name__ == '__main__':
    # This block runs only when you execute "python app.py" locally
    initialize_database()
    app.run(debug=False, host='0.0.0.0', port=5001)
else:
    # This runs when deployed (like in cPanel)
    initialize_database()
