import os, uuid
from datetime import datetime
from .extensions import db, bcrypt, login_manager
from flask_login import UserMixin

def make_shared_token():
    return uuid.uuid4().hex

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    filepath = db.Column(db.String(512), nullable=False)
    username = db.Column(db.String(128), nullable=False, default="guest")
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    size = db.Column(db.Integer, nullable=True)
    shared_token = db.Column(db.String(64), nullable=True)
    version = db.Column(db.Integer, default=1)
    category = db.Column(db.String(64), nullable=True)
    tags = db.Column(db.String(256), nullable=True)
    description = db.Column(db.String(512), nullable=True)

    def generate_share(self):
        if not self.shared_token:
            self.shared_token = make_shared_token()
        return self.shared_token

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), default="user")
    email = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


