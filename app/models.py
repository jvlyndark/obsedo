from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(64), nullable=False)  # e.g., "focus", "admin"
    is_completed = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'is_completed': self.is_completed
        }
