from flask_sqlalchemy import SQLAlchemy
import  datetime
# Database object (initialized later in app/__init__.py)
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, username, password):
        self.username = username
        self.password = password

#to_json
    def serialize(self):
        """Return object data in JSON serializable format"""
        return {
            "id": self.id,
            "username": self.username
        }
