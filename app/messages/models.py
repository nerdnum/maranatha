from app import db
from datetime import datetime


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    author = db.relationship('User')
    subject = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_private = db.Column(db.Boolean(), nullable=False, default=False)
    is_urgent = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return f"Message('{self.subject}', '{self.created_at}')"


class UserMessage(db.Model):
    __tablename__ = 'user_messages'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    message_id = db.Column(db.Integer(), db.ForeignKey('messages.id', ondelete='CASCADE'))
    sent = db.Column(db.Boolean(), nullable=False, default=False)
    read = db.Column(db.Boolean(), nullable=False, default=False)
