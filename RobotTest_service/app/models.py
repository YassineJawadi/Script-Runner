from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TestResult(db.Model):
    __tablename__ = "test_results"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
