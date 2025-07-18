from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    direction = db.Column(db.String(10), nullable=False)  # 'received' ou 'sent'
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.id} - {self.direction}>'

    def to_dict(self):
        return {
            'id': self.id,
            'contact_id': self.contact_id,
            'direction': self.direction,
            'text': self.text,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

