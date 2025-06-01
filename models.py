from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String, db.ForeignKey('chat_sessions.id'), nullable=False)
    role = db.Column(db.String)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    visible = db.Column(db.Boolean, default=True)  # 👈 Add this


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String, db.ForeignKey('chat_sessions.id'), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('chat_messages.id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)