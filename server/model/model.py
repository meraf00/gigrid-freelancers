from __future__ import annotations

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from typing import Optional

db = SQLAlchemy()


class UserType:
    FREELANCER = 'FREELANCER'
    EMPLOYER = 'FREELANCER'


class ContentType:
    TEXT = 'TEXT'
    FILE = 'FILE'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    date_of_birth = db.Column(db.DateTime)
    user_type = db.Column(db.Enum(UserType.FREELANCER, UserType.FREELANCER))
    token = db.Column(db.String(200))

    @property
    def chats(self):
        all_chats = []
        all_chats.extend(self.initiated_chats)
        all_chats.extend(self.joined_chats)
        return all_chats

    @staticmethod
    def get(user_id: int) -> Optional[User]:
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()

    def __repr__(self):
        return f"User(id={self.id}, email={self.email})"


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_1 = db.Column(db.Integer, db.ForeignKey(User.id))
    user_2 = db.Column(db.Integer, db.ForeignKey(User.id))

    u1 = db.relationship(User, backref='initiated_chats',
                         foreign_keys=[user_1])
    u2 = db.relationship(User, backref='joined_chats',
                         foreign_keys=[user_2])

    @staticmethod
    def get(chat_id: int) -> Optional[User]:
        return Chat.query.filter_by(id=chat_id).first()

    @staticmethod
    def get_chat(sender_id, receiver_id):
        chat = Chat.query.filter(
            db.or_(
                db.and_(
                    Chat.user_1 == sender_id,
                    Chat.user_2 == receiver_id
                ),
                db.and_(
                    Chat.user_1 == receiver_id,
                    Chat.user_2 == sender_id
                )
            )
        )
        return chat.first()

    def __repr__(self):
        return f"Chat(id={self.id}, user_1={self.u1.firstname}, user_2={self.u2.lastname})"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.Integer, db.ForeignKey(Chat.id), primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey(User.id))
    time_stamp = db.Column(db.DateTime, default=datetime.now)
    content = db.Column(db.String(200))
    content_type = db.Column(db.Enum(ContentType.TEXT, ContentType.FILE))

    sender = db.relationship(User, foreign_keys=[sender_id])
    chat = db.relationship(Chat, backref=db.backref(
        'messages', order_by='Message.time_stamp.desc()'), foreign_keys=[chat_id])

    @property
    def receiver(self):
        if self.chat.u1.id == self.sender_id:
            return self.chat.u2
        return self.chat.u1

    def __repr__(self):
        return f"{self.content_type.title()}(id={self.id}, chat_id={self.chat_id}, sender={self.sender.firstname}, receiver={self.receiver.firstname}, content={self.content})"
