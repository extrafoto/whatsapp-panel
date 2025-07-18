from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(10), default='bot', nullable=False)  # 'bot' ou 'humano'
    last_message_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com mensagens
    messages = db.relationship('Message', backref='contact', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Contact {self.phone_number}>'

    def to_dict(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'name': self.name,
            'status': self.status,
            'last_message_timestamp': self.last_message_timestamp.isoformat() if self.last_message_timestamp else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

