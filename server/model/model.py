from __future__ import annotations

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from typing import Optional

db = SQLAlchemy()


class UserType:
    """Data class to represent types of users involved in the system"""

    FREELANCER = 'FREELANCER'
    EMPLOYER = 'EMPLOYER'


class ContentType:
    """Data class to represent types of message contents supported by messaging functionality"""

    TEXT = 'TEXT'
    FILE = 'FILE'
    EVENT = 'EVENT'


class User(db.Model, UserMixin):
    """
    User database model

    Parameters:
        id (int): unique id that identify single user
        firstname (str): user's first name
        lastname (str): user's last name
        email (str): user's email
        password (str): user's hashed password
        date_of_birth (datetime): user's birth date
        user_type (str): one of supported user types specified under UserType class
        user_type (token): user's authentication token
        initiated_chats (list[Chat]): list of Chat objects initiated by this user
        joined_chats (list[Chat]): list of Chat objects joined by this user
    """

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    date_of_birth = db.Column(db.DateTime)
    user_type = db.Column(db.Enum(UserType.FREELANCER, UserType.EMPLOYER))
    token = db.Column(db.String(200))

    @property
    def chats(self):
        """Gets all chats associated with user

        Returns:
            list: list of Chat objects
        """

        all_chats = []
        all_chats.extend(self.initiated_chats)
        all_chats.extend(self.joined_chats)
        return all_chats

    @staticmethod
    def get(user_id: int) -> Optional[User]:
        """Gets user by id

        Args:
            user_id (int): user id

        Returns:
            User: user object if user is found, None otherwise
        """

        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        """Gets user by email

        Args:
            email (int): user email

        Returns:
            User: user object if user is found, None otherwise
        """
        return User.query.filter_by(email=email).first()

    def __repr__(self):
        return f"User(id={self.id}, email={self.email})"


class Chat(db.Model):
    """Chat database model

    Parameters:
        id (str): unique chat id
        user_1 (str): chat initiator id
        user_2 (str): second user id in chat
        u1 (User): chat initiator User object
        u2 (User): second User object
        messages (list): list of messages sent in the chat
    """

    id = db.Column(db.Integer, primary_key=True)
    user_1 = db.Column(db.Integer, db.ForeignKey(User.id))
    user_2 = db.Column(db.Integer, db.ForeignKey(User.id))

    u1 = db.relationship(User, backref='initiated_chats',
                         foreign_keys=[user_1])
    u2 = db.relationship(User, backref='joined_chats',
                         foreign_keys=[user_2])

    @staticmethod
    def get(chat_id: int) -> Optional[User]:
        """Gets chat by id

        Args:
            chat_id (int): chat id

        Returns:
            Chat: chat object if chat is found, None otherwise
        """

        return Chat.query.filter_by(id=chat_id).first()

    @staticmethod
    def get_chat(user_1, user_2):
        """Gets chat associating two users

        Args:
            user_1 (int): id of one user
            user_2 (int): id of other user

        Returns:
            Chat: chat object if chat associating the users is found, None otherwise
        """

        chat = Chat.query.filter(
            db.or_(
                db.and_(
                    Chat.user_1 == user_1,
                    Chat.user_2 == user_2
                ),
                db.and_(
                    Chat.user_1 == user_2,
                    Chat.user_2 == user_1
                )
            )
        )
        return chat.first()

    def __repr__(self):
        return f"Chat(id={self.id}, user_1={self.u1.firstname}, user_2={self.u2.lastname})"


class Message(db.Model):
    """Message database model

    Parameters:
        id (str): unique message id
        chat_id (str): chat containing two users        
        sender_id (str): the user id of sender of the message
        time_stamp (datetime): sent time
        content (str): the message sent
        content_type (str): specifies how to interpret the content
            (default is 'TEXT')
        sender (User): sender of the message
        chat (Chat): the chat the message belongs to
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.Integer, db.ForeignKey(Chat.id), primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey(User.id))
    time_stamp = db.Column(db.DateTime, default=datetime.now)
    content = db.Column(db.String(200))
    content_type = db.Column(
        db.Enum(ContentType.TEXT, ContentType.FILE, ContentType.EVENT))

    sender = db.relationship(User, foreign_keys=[sender_id])
    chat = db.relationship(Chat, backref=db.backref(
        'messages', order_by='Message.time_stamp'), foreign_keys=[chat_id])

    @property
    def receiver(self):
        """Gets receiver of message

        Returns:
            User: the recepient of message
        """

        if self.chat.u1.id == self.sender_id:
            return self.chat.u2
        return self.chat.u1

    def __repr__(self):
        return f"{self.content_type.title()}(id={self.id}, chat_id={self.chat_id}, sender={self.sender.firstname}, receiver={self.receiver.firstname}, content={self.content})"


class File(db.Model):
    """File database model

    Parameters:
        id (str): unique file id
        file_name (str): name of file
        file_path (str): path to file on local drive
        mime_type (str): MIME type of file
    """

    id = db.Column(db.String(36), primary_key=True)
    file_name = db.Column(db.String(30))
    file_path = db.Column(db.String(260))
    mime_type = db.Column(db.String(128))

    @staticmethod
    def get(file_id: str) -> Optional[File]:
        """Gets file by id

        Args:
            file_id (str): file id

        Returns:
            File: file object if file is found, None otherwise
        """

        return File.query.filter_by(id=file_id).first()

    def __repr__(self):
        return f"File(id={self.id}, file_name={self.file_name}, mime_type={self.mime_type})"


class Job(db.Model):
    id = db.Column(db.String(36), primary_key=True)


class Escrow(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    job_id = db.Column(db.String(36), db.ForeignKey(Job.id))
    worker_id = db.Column(db.String(36), db.ForeignKey(User.id))
    amount = db.Column(db.Float)

    job = db.relationship(Job, backref='escrow', foreign_keys=[job_id])
    # to = db.relationship(User, backref='escrow', foreign_keys=[worker_id])

    @staticmethod
    def get(escrow_id: str) -> Optional[Escrow]:
        """Gets escrow by id

        Args:
            escrow_id (str): escrow id

        Returns:
            Escrow: escrow object if escrow is found, None otherwise
        """

        return Escrow.query.filter_by(id=escrow_id).first()

    def __repr__(self):
        return f"Escrow(id={self.id}, job={self.job_id}, to={self.worker_id}, amount={self.amount})"
