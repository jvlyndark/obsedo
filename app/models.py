from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(16), default='medium')  # low, medium, high
    due_date = db.Column(db.DateTime, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'is_completed': self.is_completed,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None
        }
