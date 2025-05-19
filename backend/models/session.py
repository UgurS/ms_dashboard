from backend.models.base import db

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    refresh_token = db.Column(db.String(512), nullable=False, unique=True)
    user_agent = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
