from flask import request, jsonify
from .models import db, Book, Member, Category, Publisher, IssueHistory, LibraryLog
from datetime import datetime, date
import json
# import pandas as pd  # Commented out for cPanel compatibility
import os
from werkzeug.utils import secure_filename
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

            # Create book with all 12 fields
            book = Book(
                book_name=data['bookName'],
                author=data['author'],
                category_id=category.id,
                editor=data.get('editor'),
                volumes=data.get('volumes', 1),
                publisher_id=publisher.id if publisher else None,
                year=data.get('year'),
                copies=data.get('copies', 1),
                status=data.get('status', 'Available'),
                completion_status=data.get('completion_status'),
                note=data.get('note')
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

    # CSV Import endpoint
    @app.route('/api/books/import-csv', methods=['POST'])
    @token_required
    def import_books_from_csv(current_user):
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400

            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400

            if not file.filename.lower().endswith('.csv'):
                return jsonify({'error': 'File must be CSV format (.csv)'}), 400

            # Read CSV file with UTF-8 encoding for international characters
            try:
                # Save uploaded file temporarily to read with proper encoding
                import tempfile
                import os
                temp_path = None

                with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as temp_file:
                    file.save(temp_file.name)
                    temp_path = temp_file.name

                # Read CSV with UTF-8 encoding using built-in csv module
                import csv
                csv_data = []
                with open(temp_path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    csv_data = list(reader)

                # Clean up temp file
                if temp_path and os.path.exists(temp_path):
                    os.unlink(temp_path)

            except Exception as e:
                # Try with different encodings if UTF-8 fails
                try:
                    if temp_path and os.path.exists(temp_path):
                        with open(temp_path, 'r', encoding='utf-8-sig') as csvfile:
                            reader = csv.DictReader(csvfile)
                            csv_data = list(reader)
                        os.unlink(temp_path)
                except Exception as e2:
                    if temp_path and os.path.exists(temp_path):
                        os.unlink(temp_path)
                    return jsonify({'error': f'Error reading CSV file: {str(e)}. Please ensure file is saved with UTF-8 encoding.'}), 400

            # Validate required columns
            if not csv_data:
                return jsonify({'error': 'CSV file is empty or invalid'}), 400
                
            required_columns = ['Book Name', 'Author', 'Category']
            missing_columns = [col for col in required_columns if col not in csv_data[0].keys()]
            if missing_columns:
                return jsonify({'error': f'Missing required columns: {missing_columns}'}), 400

            imported_count = 0
            errors = []

            updated_count = 0

            for index, row in enumerate(csv_data):
                try:
                    # Skip empty rows (check first 3 required columns)
                    if not row.get('Book Name', '').strip() or not row.get('Author', '').strip() or not row.get('Category', '').strip():
                        continue

                    book_name = str(row['Book Name']).strip()
                    author_name = str(row['Author']).strip()

                    # Check if book already exists (by book name + author)
                    existing_book = Book.query.filter_by(
                        book_name=book_name,
                        author=author_name
                    ).first()

                    # Get or create category
                    category = Category.query.filter_by(name=str(row['Category']).strip()).first()
                    if not category:
                        category = Category(name=str(row['Category']).strip())
                        db.session.add(category)
                        db.session.flush()

                    # Get or create publisher
                    publisher = None
                    if row.get('Publisher', '').strip():
                        publisher_name = str(row['Publisher']).strip()
                        publisher = Publisher.query.filter_by(name=publisher_name).first()
                        if not publisher:
                            publisher = Publisher(name=publisher_name)
                            db.session.add(publisher)
                            db.session.flush()

                    if existing_book:
                        # UPDATE existing book with new/missing information
                        existing_book.category_id = category.id
                        existing_book.publisher_id = publisher.id if publisher else existing_book.publisher_id

                        # Update fields only if new data is provided (not empty)
                        def safe_int(value, default=None):
                            """Safely convert value to int"""
                            if not value or str(value).strip() in ['', '**', '-', 'N/A']:
                                return default
                            try:
                                return int(str(value).strip())
                            except (ValueError, TypeError):
                                return default
                        
                        def safe_str(value, default=None):
                            """Safely convert value to string"""
                            if not value or str(value).strip() in ['', '**', '-', 'N/A']:
                                return default
                            return str(value).strip()
                        
                        # Update fields with safe handling
                        editor_val = safe_str(row.get('Editor'))
                        if editor_val:
                            existing_book.editor = editor_val

                        volumes_val = safe_int(row.get('Volumes'))
                        if volumes_val:
                            existing_book.volumes = volumes_val

                        year_val = safe_int(row.get('Year'))
                        if year_val:
                            existing_book.year = year_val

                        copies_val = safe_int(row.get('Copies'))
                        if copies_val:
                            existing_book.copies = copies_val

                        status_val = safe_str(row.get('Status'))
                        if status_val:
                            existing_book.status = status_val

                        completion_val = safe_str(row.get('Completion Status'))
                        if completion_val:
                            existing_book.completion_status = completion_val

                        note_val = safe_str(row.get('Note'))
                        if note_val:
                            existing_book.note = note_val

                        updated_count += 1
                    else:
                        # CREATE new book with safe data handling
                        def safe_int(value, default=None):
                            """Safely convert value to int"""
                            if not value or str(value).strip() in ['', '**', '-', 'N/A']:
                                return default
                            try:
                                return int(str(value).strip())
                            except (ValueError, TypeError):
                                return default
                        
                        def safe_str(value, default=None):
                            """Safely convert value to string"""
                            if not value or str(value).strip() in ['', '**', '-', 'N/A']:
                                return default
                            return str(value).strip()
                        
                        book = Book(
                            book_name=book_name,
                            author=author_name,
                            category_id=category.id,
                            editor=safe_str(row.get('Editor')),
                            volumes=safe_int(row.get('Volumes'), 1),
                            publisher_id=publisher.id if publisher else None,
                            year=safe_int(row.get('Year')),
                            copies=safe_int(row.get('Copies'), 1),
                            status=safe_str(row.get('Status'), 'Available'),
                            completion_status=safe_str(row.get('Completion Status')),
                            note=safe_str(row.get('Note'))
                        )

                        db.session.add(book)
                        imported_count += 1

                except Exception as e:
                    errors.append(f'Row {index + 2}: {str(e)}')

            if imported_count > 0 or updated_count > 0:
                db.session.commit()
                if imported_count > 0:
                    add_log_entry(f'{imported_count} books imported from CSV file', 'Import')
                if updated_count > 0:
                    add_log_entry(f'{updated_count} books updated from CSV file', 'Update')

            response_data = {
                'imported_count': imported_count,
                'updated_count': updated_count,
                'message': f'Successfully imported {imported_count} new books and updated {updated_count} existing books'
            }

            if errors:
                response_data['errors'] = errors
                response_data['message'] += f' with {len(errors)} errors'

            return jsonify(response_data), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Import failed: {str(e)}'}), 500

    # CSV Template download endpoint
    @app.route('/api/books/csv-template', methods=['GET'])
    def download_csv_template():
        try:
            from flask import send_file
            import io

            # Create template data with all 12 fields including multilingual examples
            template_data = {
                'Book Name': [
                    'The Great Gatsby',
                    'গ্রেট গ্যাটসবি',  # Bengali
                    'الغَاتسبي العظيم'  # Arabic
                ],
                'Author': [
                    'F. Scott Fitzgerald',
                    'রবীন্দ্রনাথ ঠাকুর',  # Rabindranath Tagore in Bengali
                    'نجيب محفوظ'  # Naguib Mahfouz in Arabic
                ],
                'Category': [
                    'Fiction',
                    'সাহিত্য',  # Literature in Bengali
                    'أدب'  # Literature in Arabic
                ],
                'Editor': ['Maxwell Perkins', 'এডিটর নাম', 'اسم المحرر'],  # Editor names in different languages
                'Volumes': [1, 2, 1],
                'Publisher': [
                    'Scribner',
                    'বিশ্বভারতী',  # Visva-Bharati in Bengali
                    'دار الشروق'  # Dar Al-Shorouk in Arabic
                ],
                'Year': [1925, 1913, 1956],
                'Copies': [2, 1, 3],
                'Status': ['Available', 'Available', 'Available'],
                'Completion Status': ['Complete', 'Complete', 'Incomplete'],
                'Note': [
                    'Classic American novel',
                    'নোবেল পুরস্কার বিজয়ী',  # Nobel Prize winner in Bengali
                    'الرواية الكلاسيكية'  # Classic novel in Arabic
                ]
            }

            # Create CSV file in memory with UTF-8 encoding using built-in csv module
            import csv
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            headers = list(template_data.keys())
            writer.writerow(headers)
            
            # Write data rows
            num_rows = len(template_data[headers[0]])
            for i in range(num_rows):
                row = [template_data[header][i] for header in headers]
                writer.writerow(row)

            # Convert to BytesIO with UTF-8 encoding
            csv_bytes = io.BytesIO()
            csv_bytes.write(output.getvalue().encode('utf-8'))
            csv_bytes.seek(0)

            return send_file(
                csv_bytes,
                as_attachment=True,
                download_name='book_import_template.csv',
                mimetype='text/csv; charset=utf-8'
            )

        except Exception as e:
            return jsonify({'error': f'Error creating template: {str(e)}'}), 500

    # CSV Template info endpoint (for showing format info)
    @app.route('/api/books/csv-template-info', methods=['GET'])
    def get_csv_template_info():
        try:
            return jsonify({
                'message': 'CSV template format information',
                'file_format': 'CSV (.csv)',
                'encoding': 'UTF-8 (supports Arabic, Bengali, and other languages)',
                'required_columns': ['Book Name', 'Author', 'Category'],
                'optional_columns': ['Editor', 'Volumes', 'Publisher', 'Year', 'Copies', 'Status', 'Completion Status', 'Note'],
                'instructions': [
                    '1. Library ID: Auto-generated (do not include in CSV)',
                    '2. Book Name: The title of the book (Required) - Supports Arabic, Bengali, etc.',
                    '3. Author: The author name (Required) - Supports Arabic, Bengali, etc.',
                    '4. Category: Book category like Fiction, Science, etc. (Required)',
                    '5. Editor: Editor name (Optional)',
                    '6. Volumes: Number of volumes/parts (Optional, defaults to 1)',
                    '7. Publisher: Name of the publisher (Optional)',
                    '8. Year: Publication year as number (Optional)',
                    '9. Copies: Number of copies available (Optional, defaults to 1)',
                    '10. Status: Available, Issued, or Maintenance (Optional, defaults to Available)',
                    '11. Completion Status: Complete, Incomplete, In Progress, or Missing Pages (Optional)',
                    '12. Note: Any special notes about the book (Optional)'
                ],
                'multilingual_support': [
                    'CSV files support UTF-8 encoding',
                    'Perfect for Arabic text: كتاب، مؤلف، فئة',
                    'Perfect for Bengali text: বই, লেখক, বিভাগ',
                    'Save your CSV with UTF-8 encoding for best results'
                ]
            })
        except Exception as e:
            return jsonify({'error': f'Error getting template info: {str(e)}'}), 500

    # Export books to CSV endpoint
    @app.route('/api/books/export-csv', methods=['GET'])
    def export_books_to_csv():
        try:
            from flask import send_file
            import io
            import csv

            # Get all books
            books = Book.query.all()

            # Create CSV file in memory with UTF-8 encoding
            output = io.StringIO()
            writer = csv.writer(output)

            # Write CSV header
            headers = [
                'Book Name', 'Author', 'Category', 'Editor', 'Volumes', 
                'Publisher', 'Year', 'Copies', 'Status', 'Completion Status', 'Note'
            ]
            writer.writerow(headers)

            # Write book data
            for book in books:
                row = [
                    book.book_name or '',
                    book.author or '',
                    book.category.name if book.category else '',
                    book.editor or '',
                    book.volumes or 1,
                    book.publisher.name if book.publisher else '',
                    book.year or '',
                    book.copies or 1,
                    book.status or 'Available',
                    book.completion_status or '',
                    book.note or ''
                ]
                writer.writerow(row)

            # Convert StringIO to BytesIO with UTF-8 encoding
            csv_bytes = io.BytesIO()
            csv_bytes.write(output.getvalue().encode('utf-8'))
            csv_bytes.seek(0)

            return send_file(
                csv_bytes,
                as_attachment=True,
                download_name='library_books_export.csv',
                mimetype='text/csv; charset=utf-8'
            )

        except Exception as e:
            return jsonify({'error': f'Error exporting books: {str(e)}'}), 500

    # Bulk delete books endpoint
    @app.route('/api/books/bulk-delete', methods=['POST'])
    @token_required
    def bulk_delete_books(current_user):
        try:
            data = request.get_json()
            book_ids = data.get('book_ids', [])

            if not book_ids:
                return jsonify({'error': 'No book IDs provided'}), 400

            # Get books to be deleted for logging
            books_to_delete = Book.query.filter(Book.id.in_(book_ids)).all()
            deleted_count = len(books_to_delete)

            if deleted_count == 0:
                return jsonify({'error': 'No books found with provided IDs'}), 404

            # Collect book names BEFORE deletion for logging
            book_names = [book.book_name for book in books_to_delete]

            # Delete all related issue history records first
            from sqlalchemy import text
            db.session.execute(text('DELETE FROM issue_history WHERE book_id IN :book_ids'), {'book_ids': tuple(book_ids)})

            # Delete the books
            Book.query.filter(Book.id.in_(book_ids)).delete(synchronize_session=False)

            db.session.commit()

            # Log the bulk deletion
            add_log_entry(f'Bulk deleted {deleted_count} books: {", ".join(book_names[:5])}{"..." if len(book_names) > 5 else ""}', 'Delete')

            return jsonify({
                'message': f'Successfully deleted {deleted_count} books',
                'deleted_count': deleted_count
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Bulk delete failed: {str(e)}'}), 500

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
