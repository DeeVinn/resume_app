from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # admin, recruiter, etc.

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    education = db.Column(db.Text, nullable=True)
    certifications = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(100), nullable=False)  # Qualified or Unqualified
