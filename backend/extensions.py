#
# PASTE THIS ENTIRE CODE INTO: backend/extensions.py
#
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()