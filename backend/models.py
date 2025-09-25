from datetime import datetime
from .extensions import db, bcrypt



# Association table for many-to-many relationships
book_categories = db.Table('book_categories',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

book_publishers = db.Table('book_publishers',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('publisher_id', db.Integer, db.ForeignKey('publisher.id'), primary_key=True)
)

class Book(db.Model):
    # 1. library_id (auto-generated primary key)
    id = db.Column(db.Integer, primary_key=True)

    # 2. book_name (required)
    book_name = db.Column(db.String(200), nullable=False)

    # 3. author (required)
    author = db.Column(db.String(100), nullable=False)

    # 4. category (required)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    # 5. editor (optional)
    editor = db.Column(db.String(100))

    # 6. volumes (optional, default 1)
    volumes = db.Column(db.Integer, default=1)

    # 7. publisher_id (optional)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'))

    # 8. year (optional)
    year = db.Column(db.Integer)

    # 9. copies (optional, default 1)
    copies = db.Column(db.Integer, default=1)

    # 10. status (optional, default Available)
    status = db.Column(db.String(20), default='Available')  # Available, Issued

    # 11. completion_status (optional)
    completion_status = db.Column(db.String(50))  # Complete, Incomplete, In Progress, etc.

    # 12. note (optional)
    note = db.Column(db.Text)

    # System fields
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = db.relationship('Category', backref='books')
    publisher = db.relationship('Publisher', backref='books')
    issue_records = db.relationship('IssueHistory', backref='book', lazy='dynamic')

    def to_dict(self):
        return {
            'library_id': self.id,
            'bookName': self.book_name,
            'author': self.author,
            'category': self.category.name if self.category else None,
            'editor': self.editor,
            'volumes': self.volumes,
            'publisher': self.publisher.name if self.publisher else None,
            'year': self.year,
            'copies': self.copies,
            'status': self.status,
            'completion_status': self.completion_status,
            'note': self.note,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    issue_records = db.relationship('IssueHistory', backref='member', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.Text)
    contact_info = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'contact_info': self.contact_info,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class IssueHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)  # Expected return date
    actual_return_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='Pending')  # Pending, Returned
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'bookName': self.book.book_name if self.book else None,
            'memberName': self.member.name if self.member else None,
            'issueDate': self.issue_date.isoformat() if self.issue_date else None,
            'returnDate': self.return_date.isoformat() if self.return_date else None,
            'actualReturnDate': self.actual_return_date.isoformat() if self.actual_return_date else None,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class LibraryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    log_type = db.Column(db.String(50), default='General')  # General, Book, Member, etc.
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None,
            'content': self.content,
            'log_type': self.log_type
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


