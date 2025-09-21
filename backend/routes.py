from flask import request, jsonify
from .models import db, Book, Member, Category, Publisher, IssueHistory, LibraryLog
from datetime import datetime, date
import json
from sqlalchemy.exc import IntegrityError
from .utils import token_required

def register_routes(app):
    # Utility function to add log entries
    def add_log_entry(content, log_type='General'):
        log = LibraryLog(content=content, log_type=log_type)
        db.session.add(log)
        db.session.commit()

    # Dashboard API  
    @app.route('/api/dashboard', methods=['GET'])
    def get_dashboard_stats():
        try:
            total_books = Book.query.count()
            total_authors = db.session.query(Book.author).distinct().count()
            total_categories = Category.query.count()
            books_available = Book.query.filter_by(status='Available').count()
            books_issued = Book.query.filter_by(status='Issued').count()
            
            return jsonify({
                'total_books': total_books,
                'total_authors': total_authors,
                'total_categories': total_categories,
                'books_available': books_available,
                'books_issued': books_issued
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Books API
    @app.route('/api/books', methods=['GET'])
    def get_books():
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 100, type=int)
            
            # Get filter parameters
            book_name = request.args.get('bookName', '')
            author = request.args.get('author', '')
            category = request.args.get('category', '')
            publisher = request.args.get('publisher', '')
            status = request.args.get('status', '')
            
            # Build query with filters
            query = Book.query
            
            if book_name:
                query = query.filter(Book.book_name.ilike(f'%{book_name}%'))
            if author:
                query = query.filter(Book.author.ilike(f'%{author}%'))
            if category:
                query = query.join(Category).filter(Category.name.ilike(f'%{category}%'))
            if publisher:
                query = query.join(Publisher).filter(Publisher.name.ilike(f'%{publisher}%'))
            if status:
                query = query.filter(Book.status == status)
            
            # Pagination
            pagination = query.paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            books = [book.to_dict() for book in pagination.items]
            
            return jsonify({
                'books': books,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page,
                'per_page': per_page
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Members API
    @app.route('/api/members', methods=['GET'])
    def get_members():
        try:
            members = Member.query.all()
            return jsonify([member.to_dict() for member in members])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Categories API
    @app.route('/api/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            return jsonify([category.to_dict() for category in categories])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Publishers API
    @app.route('/api/publishers', methods=['GET'])
    def get_publishers():
        try:
            publishers = Publisher.query.all()
            return jsonify([publisher.to_dict() for publisher in publishers])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Issue History API
    @app.route('/api/issue-history', methods=['GET'])
    def get_issue_history():
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 100, type=int)
            
            pagination = IssueHistory.query.paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            history = [record.to_dict() for record in pagination.items]
            
            return jsonify({
                'history': history,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page,
                'per_page': per_page
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Library Log API
    @app.route('/api/library-log', methods=['GET'])
    def get_library_log():
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 100, type=int)
            
            query = LibraryLog.query.order_by(LibraryLog.timestamp.desc())
            
            pagination = query.paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            logs = [log.to_dict() for log in pagination.items]
            
            return jsonify({
                'logs': logs,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page,
                'per_page': per_page
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'Library Management System API is running'})

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
