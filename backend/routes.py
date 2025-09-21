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

    @app.route('/api/books', methods=['POST'])
    @token_required
    def add_book(current_user):
        try:
            data = request.get_json()
            
            # Validate required fields
            if not data.get('bookName') or not data.get('author') or not data.get('category'):
                return jsonify({'error': 'Book name, author, and category are required'}), 400
            
            # Get or create category
            category = Category.query.filter_by(name=data['category']).first()
            if not category:
                category = Category(name=data['category'])
                db.session.add(category)
                db.session.flush()
            
            # Get or create publisher
            publisher = None
            if data.get('publisher'):
                publisher = Publisher.query.filter_by(name=data['publisher']).first()
                if not publisher:
                    publisher = Publisher(name=data['publisher'])
                    db.session.add(publisher)
                    db.session.flush()
            
            # Create book
            book = Book(
                book_name=data['bookName'],
                author=data['author'],
                volumes=data.get('volumes', 1),
                category_id=category.id,
                publisher_id=publisher.id if publisher else None,
                year=data.get('year'),
                note=data.get('note'),
                status='Available'
            )
            
            db.session.add(book)
            db.session.commit()
            
            add_log_entry(f'New book "{data["bookName"]}" added to library', 'Book')
            
            return jsonify(book.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/books/<int:book_id>', methods=['GET'])
    def get_book(book_id):
        try:
            book = Book.query.get_or_404(book_id)
            return jsonify(book.to_dict())
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/books/<int:book_id>', methods=['PUT'])
    @token_required
    def update_book(current_user, book_id):
        try:
            book = Book.query.get_or_404(book_id)
            data = request.get_json()
            
            # Update fields
            if 'bookName' in data:
                book.book_name = data['bookName']
            if 'author' in data:
                book.author = data['author']
            if 'volumes' in data:
                book.volumes = data['volumes']
            if 'category' in data:
                category = Category.query.filter_by(name=data['category']).first()
                if not category:
                    category = Category(name=data['category'])
                    db.session.add(category)
                    db.session.flush()
                book.category_id = category.id
            if 'publisher' in data:
                if data['publisher']:
                    publisher = Publisher.query.filter_by(name=data['publisher']).first()
                    if not publisher:
                        publisher = Publisher(name=data['publisher'])
                        db.session.add(publisher)
                        db.session.flush()
                    book.publisher_id = publisher.id
                else:
                    book.publisher_id = None
            if 'year' in data:
                book.year = data['year']
            if 'note' in data:
                book.note = data['note']
            
            book.updated_at = datetime.utcnow()
            db.session.commit()
            
            add_log_entry(f'Book "{book.book_name}" details updated', 'Book')
            
            return jsonify(book.to_dict())
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/books/<int:book_id>', methods=['DELETE'])
    @token_required
    def delete_book(current_user, book_id):
        try:
            book = Book.query.get_or_404(book_id)
            book_name = book.book_name
            
            db.session.delete(book)
            db.session.commit()
            
            add_log_entry(f'Book "{book_name}" deleted from library', 'Book')
            
            return jsonify({'message': 'Book deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # Issue/Return Books
    @app.route('/api/books/<int:book_id>/issue', methods=['POST'])
    @token_required
    def issue_book(current_user, book_id):
        try:
            book = Book.query.get_or_404(book_id)
            data = request.get_json()
            
            if book.status == 'Issued':
                return jsonify({'error': 'Book is already issued'}), 400
            
            # Get member
            member = Member.query.filter_by(name=data['memberName']).first()
            if not member:
                return jsonify({'error': 'Member not found'}), 404
            
            # Create issue record
            issue_record = IssueHistory(
                book_id=book.id,
                member_id=member.id,
                issue_date=datetime.strptime(data['issueDate'], '%Y-%m-%d').date(),
                return_date=datetime.strptime(data['returnDate'], '%Y-%m-%d').date(),
                status='Pending'
            )
            
            # Update book status
            book.status = 'Issued'
            
            db.session.add(issue_record)
            db.session.commit()
            
            add_log_entry(f'Book "{book.book_name}" issued to {member.name}. Expected return: {data["returnDate"]}', 'Issue')
            
            return jsonify(issue_record.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/books/<int:book_id>/return', methods=['POST'])
    @token_required
    def return_book(current_user, book_id):
        try:
            book = Book.query.get_or_404(book_id)
            data = request.get_json()
            
            if book.status == 'Available':
                return jsonify({'error': 'Book is already available'}), 400
            
            # Find pending issue record
            issue_record = IssueHistory.query.filter_by(
                book_id=book.id, 
                status='Pending'
            ).first()
            
            if not issue_record:
                return jsonify({'error': 'No pending issue record found'}), 404
            
            # Update issue record
            issue_record.status = 'Returned'
            issue_record.actual_return_date = datetime.strptime(data['actualReturnDate'], '%Y-%m-%d').date()
            
            # Update book status
            book.status = 'Available'
            
            db.session.commit()
            
            add_log_entry(f'Book "{book.book_name}" returned by {issue_record.member.name} on {data["actualReturnDate"]}', 'Return')
            
            return jsonify(issue_record.to_dict())
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # Members API
    @app.route('/api/members', methods=['GET'])
    def get_members():
        try:
            members = Member.query.all()
            return jsonify([member.to_dict() for member in members])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/members', methods=['POST'])
    @token_required
    def add_member(current_user):
        try:
            data = request.get_json()
            
            if not data.get('name'):
                return jsonify({'error': 'Member name is required'}), 400
            
            member = Member(
                name=data['name'],
                email=data.get('email'),
                phone=data.get('phone'),
                address=data.get('address')
            )
            
            db.session.add(member)
            db.session.commit()
            
            add_log_entry(f'New member "{data["name"]}" added', 'Member')
            
            return jsonify(member.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/members/<int:member_id>', methods=['DELETE'])
    @token_required
    def delete_member(current_user, member_id):
        try:
            member = Member.query.get_or_404(member_id)
            member_name = member.name
            
            # Check if member has pending issues
            pending_issues = IssueHistory.query.filter_by(
                member_id=member_id, 
                status='Pending'
            ).count()
            
            if pending_issues > 0:
                return jsonify({'error': f'Cannot delete member with {pending_issues} pending book issues'}), 400
            
            db.session.delete(member)
            db.session.commit()
            
            add_log_entry(f'Member "{member_name}" deleted', 'Member')
            
            return jsonify({'message': 'Member deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # Categories API
    @app.route('/api/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            return jsonify([category.to_dict() for category in categories])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/categories', methods=['POST'])
    @token_required
    def add_category(current_user):
        try:
            data = request.get_json()
            
            if not data.get('name'):
                return jsonify({'error': 'Category name is required'}), 400
            
            category = Category(
                name=data['name'],
                description=data.get('description')
            )
            
            db.session.add(category)
            db.session.commit()
            
            add_log_entry(f'New category "{data["name"]}" added', 'Category')
            
            return jsonify(category.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/categories/<int:category_id>', methods=['PUT'])
    @token_required
    def update_category(current_user, category_id):
        try:
            category = Category.query.get_or_404(category_id)
            data = request.get_json()
            
            if 'name' in data:
                # Check if new name already exists
                existing = Category.query.filter_by(name=data['name']).first()
                if existing and existing.id != category_id:
                    return jsonify({'error': 'Category with this name already exists'}), 400
                category.name = data['name']
            
            if 'description' in data:
                category.description = data['description']
            
            db.session.commit()
            
            add_log_entry(f'Category "{category.name}" updated', 'Category')
            
            return jsonify(category.to_dict())
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/categories/<int:category_id>', methods=['DELETE'])
    @token_required
    def delete_category(current_user, category_id):
        try:
            category = Category.query.get_or_404(category_id)
            category_name = category.name
            
            # Check if category is used by books
            books_count = Book.query.filter_by(category_id=category_id).count()
            if books_count > 0:
                return jsonify({'error': f'Cannot delete category used by {books_count} books'}), 400
            
            db.session.delete(category)
            db.session.commit()
            
            add_log_entry(f'Category "{category_name}" deleted', 'Category')
            
            return jsonify({'message': 'Category deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # Publishers API
    @app.route('/api/publishers', methods=['GET'])
    def get_publishers():
        try:
            publishers = Publisher.query.all()
            return jsonify([publisher.to_dict() for publisher in publishers])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/publishers', methods=['POST'])
    @token_required
    def add_publisher(current_user):
        try:
            data = request.get_json()
            
            if not data.get('name'):
                return jsonify({'error': 'Publisher name is required'}), 400
            
            publisher = Publisher(
                name=data['name'],
                address=data.get('address'),
                contact_info=data.get('contact_info')
            )
            
            db.session.add(publisher)
            db.session.commit()
            
            add_log_entry(f'New publisher "{data["name"]}" added', 'Publisher')
            
            return jsonify(publisher.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/publishers/<int:publisher_id>', methods=['PUT'])
    @token_required
    def update_publisher(current_user, publisher_id):
        try:
            publisher = Publisher.query.get_or_404(publisher_id)
            data = request.get_json()
            
            if 'name' in data:
                # Check if new name already exists
                existing = Publisher.query.filter_by(name=data['name']).first()
                if existing and existing.id != publisher_id:
                    return jsonify({'error': 'Publisher with this name already exists'}), 400
                publisher.name = data['name']
            
            if 'address' in data:
                publisher.address = data['address']
            if 'contact_info' in data:
                publisher.contact_info = data['contact_info']
            
            db.session.commit()
            
            add_log_entry(f'Publisher "{publisher.name}" updated', 'Publisher')
            
            return jsonify(publisher.to_dict())
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/publishers/<int:publisher_id>', methods=['DELETE'])
    @token_required
    def delete_publisher(current_user, publisher_id):
        try:
            publisher = Publisher.query.get_or_404(publisher_id)
            publisher_name = publisher.name
            
            # Check if publisher is used by books
            books_count = Book.query.filter_by(publisher_id=publisher_id).count()
            if books_count > 0:
                return jsonify({'error': f'Cannot delete publisher used by {books_count} books'}), 400
            
            db.session.delete(publisher)
            db.session.commit()
            
            add_log_entry(f'Publisher "{publisher_name}" deleted', 'Publisher')
            
            return jsonify({'message': 'Publisher deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/members/<int:member_id>', methods=['PUT'])
    @token_required
    def update_member(current_user, member_id):
        try:
            member = Member.query.get_or_404(member_id)
            data = request.get_json()
            
            if 'name' in data:
                # Check if new name already exists
                existing = Member.query.filter_by(name=data['name']).first()
                if existing and existing.id != member_id:
                    return jsonify({'error': 'Member with this name already exists'}), 400
                member.name = data['name']
            
            if 'email' in data:
                member.email = data['email']
            if 'phone' in data:
                member.phone = data['phone']
            if 'address' in data:
                member.address = data['address']
            
            db.session.commit()
            
            add_log_entry(f'Member "{member.name}" details updated', 'Member')
            
            return jsonify(member.to_dict())
        except Exception as e:
            db.session.rollback()
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
