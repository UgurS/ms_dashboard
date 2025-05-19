import secrets
from flask_jwt_extended import create_access_token, create_refresh_token
from backend.models.admin import Admin
from backend.models.session import Session
from backend.models.base import db
from werkzeug.security import check_password_hash
from flask import request


class AuthService:
    def login(self, username, password):
        admin = Admin.query.filter_by(username=username).first()
        if not admin or not check_password_hash(admin.password_hash, password):
            return None, "Invalid credentials"

        access_token = create_access_token(identity=str(admin.id))
        refresh_token = create_refresh_token(identity=str(admin.id))

        session = Session(
            admin_id=admin.id,
            refresh_token=refresh_token,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(session)
        db.session.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }, None

    def refresh_session(self, old_refresh_token):
        session = Session.query.filter_by(refresh_token=old_refresh_token).first()
        if not session:
            return None, "Invalid refresh token"

        # Issue new access and refresh token
        new_access_token = create_access_token(identity=str(session.admin_id))
        new_refresh_token = create_refresh_token(identity=str(session.admin_id))

        session.refresh_token = new_refresh_token  # rotate
        db.session.commit()

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }, None

    def logout(self, refresh_token):
        session = Session.query.filter_by(refresh_token=refresh_token).first()
        if session:
            db.session.delete(session)
            db.session.commit()
        return True