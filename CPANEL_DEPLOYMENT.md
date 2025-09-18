# 🚀 cPanel Deployment Guide for Library Management System

## 📋 Pre-Deployment Checklist

✅ **Local Setup Complete:**
- Single 'library' database created
- MySQL migration successful  
- Application tested and working
- All files organized in backend folder

## 🔧 Step 1: cPanel MySQL Database Setup

### 1.1 Create MySQL Database in cPanel
1. **Login to cPanel**
2. **Go to "MySQL Databases"**
3. **Create Database:**
   - Database Name: `library` (or `yourdomain_library`)
   - Click "Create Database"

### 1.2 Create MySQL User
1. **Create Database User:**
   - Username: `lms_user` (or your preferred name)
   - Password: `your_secure_password`
   - Click "Create User"

### 1.3 Add User to Database
1. **Add User to Database:**
   - Select User: `lms_user`
   - Select Database: `library`
   - Check "ALL PRIVILEGES"
   - Click "Make Changes"

## 🌐 Step 2: Upload Application Files

### 2.1 File Upload
1. **Upload all project files** to your domain folder (usually `public_html`)
2. **Maintain folder structure:**
   ```
   public_html/
   ├── app.py
   ├── backend/
   ├── css/
   ├── js/
   ├── index.html
   ├── requirements.txt
   └── (all other files)
   ```

## ⚙️ Step 3: Environment Configuration

### 3.1 Create .env file in cPanel
Create a file named `.env` in your root directory:

```bash
# cPanel MySQL Configuration
DATABASE_URL=mysql+pymysql://YOUR_DB_USER:YOUR_DB_PASSWORD@localhost/YOUR_DB_NAME
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here

# Example:
# DATABASE_URL=mysql+pymysql://mydomain_lmsuser:mypassword@localhost/mydomain_library
# FLASK_ENV=production
# SECRET_KEY=mysecretkey123
```

### 3.2 Update Your Database Connection String
**Replace these values in your .env file:**
- `YOUR_DB_USER` → Your cPanel MySQL username
- `YOUR_DB_PASSWORD` → Your MySQL user password  
- `YOUR_DB_NAME` → Your cPanel database name

**Example:**
```bash
DATABASE_URL=mysql+pymysql://johndoe_lmsuser:mypassword123@localhost/johndoe_library
```

## 🐍 Step 4: Python Environment Setup

### 4.1 Install Python Packages
In cPanel Terminal or SSH:
```bash
pip install -r requirements.txt
```

### 4.2 Test Database Connection
```bash
python -c "from app import app; from backend.extensions import db; app.app_context().push(); db.create_all(); print('✅ Database setup complete!')"
```

## 🚀 Step 5: Application Startup

### 5.1 Run the Application
```bash
python app.py
```

### 5.2 Set Up as Service (Optional)
For production, you might want to use:
- **Passenger** (if supported by your host)
- **PM2** for Node.js-style process management
- **systemd** service (if you have root access)

## 🔒 Step 6: Security & Production Settings

### 6.1 Update Secret Key
- Generate a strong SECRET_KEY
- Never use default keys in production

### 6.2 Database Security
- Use strong passwords
- Limit database user privileges
- Enable SSL if available

## 🧪 Step 7: Testing Deployment

### 7.1 Test Checklist
- ✅ Application loads at your domain
- ✅ Database connection works
- ✅ All API endpoints respond
- ✅ CRUD operations work
- ✅ File uploads/downloads work

### 7.2 Common URLs to Test
```
https://yourdomain.com/           # Main application
https://yourdomain.com/api/health # API health check
https://yourdomain.com/api/dashboard # Dashboard data
```

## 🔧 Troubleshooting

### Common Issues:

**1. Database Connection Error:**
- Check DATABASE_URL format
- Verify MySQL user permissions
- Confirm database name matches

**2. Import Errors:**
- Ensure all requirements.txt packages installed
- Check Python version compatibility

**3. Permission Errors:**
- Check file permissions (755 for directories, 644 for files)
- Verify cPanel user has access to files

**4. Static Files Not Loading:**
- Check file paths in HTML
- Verify CSS/JS files uploaded correctly

## 📞 Support Commands

### Check Database Connection:
```bash
python -c "import pymysql; print('PyMySQL installed:', pymysql.VERSION)"
```

### Test Environment Variables:
```bash
python -c "import os; print('DATABASE_URL:', os.environ.get('DATABASE_URL', 'Not set'))"
```

### Check Flask App:
```bash
python -c "from app import app; print('Flask app loaded successfully!')"
```

## 🎉 Success!

Once deployed successfully:
- ✅ Your Library Management System will be live on the internet
- ✅ MySQL database will automatically create tables on first run
- ✅ All your library data will be safely stored in cPanel MySQL
- ✅ Multiple users can access simultaneously

**Your application is now production-ready!** 🚀

---

**Need help?** Check the error logs in cPanel or contact your hosting provider for Python/Flask support.
