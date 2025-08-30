from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    age = db.Column(db.Integer)
    fitness_level = db.Column(db.String(20))
    health_goals = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    wellness_plans = db.relationship('WellnessPlan', backref='user', lazy=True)
    mood_logs = db.relationship('MoodLog', backref='user', lazy=True)
    feelings_logs = db.relationship('FeelingsLog', backref='user', lazy=True)  # Added this

class WellnessPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mental_health_plan = db.Column(db.Text)
    fitness_plan = db.Column(db.Text)
    nutrition_plan = db.Column(db.Text)
    personalized_insights = db.Column(db.Text)  # New field
    motivation_message = db.Column(db.Text)     # New field
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class MoodLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood_score = db.Column(db.Integer)  # 1-10 scale
    stress_level = db.Column(db.Integer)  # 1-10 scale
    energy_level = db.Column(db.Integer)  # 1-10 scale
    notes = db.Column(db.Text)
    log_date = db.Column(db.DateTime, default=datetime.utcnow)

class FeelingsLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feelings_text = db.Column(db.Text, nullable=False)
    ai_analysis = db.Column(db.Text)  # Store AI analysis as JSON
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class VRContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content_type = db.Column(db.String(20))  # meditation, therapy, exercise
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)  # in minutes
    difficulty_level = db.Column(db.String(20))
    file_path = db.Column(db.String(200))
