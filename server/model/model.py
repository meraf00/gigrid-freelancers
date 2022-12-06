from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from typing import Optional

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    date_of_birth = db.Column(db.DateTime)

    @staticmethod
    def get(user_id: int) -> Optional[User]:
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def authenticate(email: str, password: str) -> bool:
        user = User.get_by_email(email)
        if not user:
            return False
        print(user.password, password,
              check_password_hash(user.password, password))
        return check_password_hash(user.password, password)

    def __repr__(self):
        return f"User(id={self.id}, email={self.email})"
