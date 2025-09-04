# Library Management System - Flask Backend

A robust Flask-based REST API backend for the Library Management System.

## Features

- **Books Management**: CRUD operations for books with categories and publishers
- **Members Management**: Add, edit, and delete library members
- **Categories & Publishers**: Manage book categories and publishers
- **Issue History**: Track book borrowing and returns
- **Library Logs**: Comprehensive logging of all system activities
- **RESTful API**: Clean, RESTful API design with proper HTTP status codes
- **Database**: SQLite database with SQLAlchemy ORM
- **CORS Support**: Cross-origin resource sharing enabled for frontend integration

## Project Structure

```
├── app.py              # Main Flask application
├── models.py           # Database models and relationships
├── routes.py           # API routes and endpoints
├── config.py           # Configuration settings
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── library.db          # SQLite database (created automatically)
└── README_BACKEND.md   # This file
```

## Database Schema

### Core Tables
- **Book**: Books with metadata (name, author, category, publisher, etc.)
- **Member**: Library members with contact information
- **Category**: Book categories (Fiction, Non-Fiction, Science, etc.)
- **Publisher**: Book publishers
- **IssueHistory**: Book borrowing records
- **LibraryLog**: System activity logs

### Relationships
- Books belong to Categories and Publishers
- IssueHistory links Books and Members
- All operations are logged in LibraryLog

## API Endpoints

### Dashboard
- `GET /api/dashboard` - Get dashboard statistics

### Books
- `GET /api/books` - List books with pagination and filtering
- `POST /api/books` - Add new book
- `GET /api/books/<id>` - Get specific book
- `PUT /api/books/<id>` - Update book
- `DELETE /api/books/<id>` - Delete book
- `POST /api/books/<id>/issue` - Issue book to member
- `POST /api/books/<id>/return` - Return book

### Members
- `GET /api/members` - List all members
- `POST /api/members` - Add new member
- `PUT /api/members/<id>` - Update member
- `DELETE /api/members/<id>` - Delete member

### Categories
- `GET /api/categories` - List all categories
- `POST /api/categories` - Add new category
- `PUT /api/categories/<id>` - Update category
- `DELETE /api/categories/<id>` - Delete category

### Publishers
- `GET /api/publishers` - List all publishers
- `POST /api/publishers` - Add new publisher
- `PUT /api/publishers/<id>` - Update publisher
- `DELETE /api/publishers/<id>` - Delete publisher

### Issue History
- `GET /api/issue-history` - List issue history with pagination and filtering

### Library Logs
- `GET /api/library-log` - List library logs with pagination
- `POST /api/library-log` - Add new log entry

### Health Check
- `GET /api/health` - API health status

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables (Optional)
```bash
# For development (default)
export FLASK_ENV=development

# For production
export FLASK_ENV=production
export DATABASE_URL=your_production_db_url
export SECRET_KEY=your_secret_key
```

### 3. Initialize Database
```bash
python init_db.py
```

### 4. Run the Application
```bash
python app.py
```

The API will be available at `http://localhost:5001`

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python app.py
```

### Database Operations
```bash
# Initialize database
python init_db.py

# Access Flask shell
flask shell

# In Flask shell, you can:
from app import db
from models import Book, Member, Category, Publisher
# Query and manipulate data
```

### API Testing

You can test the API endpoints using tools like:
- **Postman**: Import the API endpoints
- **cURL**: Command-line testing
- **Frontend**: The existing HTML/JS frontend

#### Example API Calls

**Get all books:**
```bash
curl http://localhost:5000/api/books
```

**Add a new book:**
```bash
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "bookName": "Sample Book",
    "author": "Sample Author",
    "category": "Fiction",
    "publisher": "Sample Publisher",
    "year": 2024
  }'
```

**Issue a book:**
```bash
curl -X POST http://localhost:5000/api/books/1/issue \
  -H "Content-Type: application/json" \
  -d '{
    "memberName": "John Doe",
    "issueDate": "2024-01-15",
    "returnDate": "2024-02-15"
  }'
```

## Configuration

### Development Configuration
- SQLite database (`library.db`)
- Debug mode enabled
- CORS enabled for frontend development

### Production Configuration
- Use environment variables for database URL
- Debug mode disabled
- Configure proper CORS origins

### Environment Variables
- `FLASK_ENV`: Environment (development/production/testing)
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Flask secret key

## Database Features

### Automatic Logging
All major operations are automatically logged:
- Book additions, updates, deletions
- Member management
- Book issues and returns
- Category and publisher changes

### Data Integrity
- Foreign key constraints
- Validation checks before deletion
- Transaction rollback on errors

### Sample Data
The system comes with pre-populated sample data:
- 10 book categories
- 9 publishers
- 5 sample members
- 3 sample books
- Initial library logs

## Error Handling

The API includes comprehensive error handling:
- **400 Bad Request**: Invalid input data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side errors
- **Validation Errors**: Detailed error messages
- **Database Rollback**: Automatic rollback on errors

## Security Features

- Input validation and sanitization
- SQL injection prevention via SQLAlchemy
- CORS configuration for frontend security
- Environment-based configuration

## Performance Features

- Database query optimization
- Pagination for large datasets
- Efficient relationship loading
- Connection pooling (with production databases)

## Monitoring and Logging

- Comprehensive activity logging
- Error tracking and reporting
- Health check endpoint
- Database operation logging

## Future Enhancements

- User authentication and authorization
- Advanced search and filtering
- Export functionality (CSV, Excel)
- Email notifications
- Fine calculation for late returns
- Backup and restore functionality
- API rate limiting
- Request/response logging

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure SQLite is accessible
   - Check file permissions for `library.db`

2. **Import Errors**
   - Verify all dependencies are installed
   - Check Python path and virtual environment

3. **CORS Issues**
   - Verify CORS is properly configured
   - Check frontend origin settings

4. **Sample Data Not Loading**
   - Run `python init_db.py` manually
   - Check database file permissions

### Debug Mode
Enable debug mode for detailed error messages:
```bash
export FLASK_ENV=development
python app.py
```

## Support

For issues and questions:
1. Check the error logs
2. Verify database connectivity
3. Test individual API endpoints
4. Review configuration settings

## License

This project is part of the Library Management System.
