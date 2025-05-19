# scripts/create_admin.py

import sys
import os
import hashlib
import uuid
from getpass import getpass

from backend import create_app
from backend.models.base import db
from backend.models.admin import Admin
from werkzeug.security import generate_password_hash

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = create_app()

with app.app_context():
    username = input("Enter admin username: ").strip()
    if not username:
        print("Username cannot be empty.")
        sys.exit(1)

    password = getpass("Enter admin password: ").strip()
    confirm = getpass("Confirm password: ").strip()

    if password != confirm:
        print("Passwords do not match.")
        sys.exit(1)

    if not password:
        print("Password cannot be empty.")
        sys.exit(1)

    # Check if admin exists
    if Admin.query.filter_by(username=username).first():
        print(f"⚠Admin '{username}' already exists.")
        sys.exit(0)

    hashed_pw = generate_password_hash(password)

    admin = Admin(
        username=username,
        password_hash=hashed_pw
    )

    db.session.add(admin)
    db.session.commit()
    print(f"Admin '{username}' created successfully.")
