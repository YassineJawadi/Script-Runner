from . import db
from flask_login import UserMixin
from passlib.hash import sha256_crypt
from datetime import datetime
from sqlalchemy.dialects.mysql import ENUM
import secrets


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    api_key = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    role = db.Column(ENUM("QA ENGINEER", "PROJECT MANAGER", "QA Tester", name="user_roles"), default="QA Tester", nullable=False)
    is_authenticated = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"


    def set_password(self, password):
        self.password = sha256_crypt.hash(password)

    def verify_password(self, password):
        return sha256_crypt.verify(password, self.password)


    def encode_api_key(self):
        self.api_key = secrets.token_hex(32)
        return self.api_key


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "api_key": self.api_key,
        }
