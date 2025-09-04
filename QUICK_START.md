# Quick Start Guide - Library Management System Backend

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
**Option A: Windows Batch File**
```bash
start_server.bat
```

**Option B: PowerShell**
```bash
.\start_server.ps1
```

**Option C: Manual**
```bash
python init_db.py
python app.py
```

### 3. Test the API
Open a new terminal and run:
```bash
python test_api.py
```

### 4. Access the API
- **API Base URL**: http://localhost:5001/api
- **Health Check**: http://localhost:5001/api/health
- **Dashboard**: http://localhost:5001/api/dashboard
- **Books**: http://localhost:5001/api/books

## 📚 What's Included

✅ **Complete REST API** with all CRUD operations  
✅ **SQLite Database** with sample data  
✅ **Automatic Logging** of all operations  
✅ **CORS Support** for frontend integration  
✅ **Error Handling** with proper HTTP status codes  
✅ **Pagination** for large datasets  
✅ **Filtering** and search capabilities  

## 🔧 Database Schema

- **Books**: Name, author, category, publisher, status
- **Members**: Name, email, phone, address
- **Categories**: Fiction, Non-Fiction, Science, etc.
- **Publishers**: Penguin, Random House, etc.
- **Issue History**: Book borrowing records
- **Library Logs**: System activity tracking

## 🧪 Test the Endpoints

### Get All Books
```bash
curl http://localhost:5001/api/books
```

### Add a New Book
```bash
curl -X POST http://localhost:5001/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "bookName": "Test Book",
    "author": "Test Author",
    "category": "Fiction"
  }'
```

### Get Dashboard Stats
```bash
curl http://localhost:5001/api/dashboard
```

## 🌐 Frontend Integration

The API is designed to work with your existing HTML/JS frontend. Just update the frontend to make API calls instead of using local data.

## 🚨 Troubleshooting

**Port already in use?**
- Change port in `app.py` or kill existing process

**Database errors?**
- Delete `library.db` and run `python init_db.py` again

**Import errors?**
- Ensure all requirements are installed: `pip install -r requirements.txt`

**CORS issues?**
- Check that CORS is enabled in the frontend

## 📖 Next Steps

1. **Test all endpoints** using the test script
2. **Integrate with frontend** by updating API calls
3. **Customize the models** if needed
4. **Add authentication** for production use
5. **Deploy to production** with proper database

## 🆘 Need Help?

- Check the detailed `README_BACKEND.md`
- Review error messages in the terminal
- Test individual endpoints with curl or Postman
- Verify database file permissions

---

**🎉 You're all set! The Flask backend is running and ready to use.**
