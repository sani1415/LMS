#
# PASTE THIS ENTIRE CODE INTO: app.py
#
import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.config import config
from backend.extensions import db, bcrypt
from backend.models import Book, User, Category, Publisher, Member # Import models


# Determine the config name from the environment variable
config_name = os.environ.get('FLASK_ENV', 'default')

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config[config_name])

# Check if ProductionConfig is being used but database URI is None
if config_name == 'production' and app.config.get('SQLALCHEMY_DATABASE_URI') is None:
    raise ValueError("Production configuration requires database environment variables (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME) to be set in cPanel.")

# Initialize extensions with the app
db.init_app(app)
bcrypt.init_app(app)
CORS(app)  # Enable CORS for frontend integration

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
                Book(book_name='Sample Fiction Book', author='Sample Author', 
                     category_id=fiction_cat.id if fiction_cat else 1,
                     publisher_id=penguin_pub.id if penguin_pub else 1,
                     year=2023, volumes=1),
                Book(book_name='Sample Science Book', author='Science Author',
                     category_id=science_cat.id if science_cat else 2,
                     publisher_id=penguin_pub.id if penguin_pub else 1,
                     year=2023, volumes=1)
            ]
            for book in books:
                db.session.add(book)
        
        db.session.commit()
        print("Sample data created successfully")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.session.rollback()

if __name__ == '__main__':
    # This block runs only when you execute "python app.py" locally
    with app.app_context():
        db.create_all()  # Create database tables
        # Add sample data if the database is empty
        if not Book.query.first():
            print("Database is empty, creating sample data...")
            create_sample_data()
            print("Sample data created.")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
