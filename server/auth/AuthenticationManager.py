import os
import sys
from functools import wraps
from typing import Any

from itsdangerous.url_safe import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, SignatureExpired
from werkzeug.security import check_password_hash

from model import User

sys.path.append('..')


class AuthenticationManager:
    def __init__(self, key: str, max_age: int = 604800) -> None:
        """
        key: key used for encryption
        max_age: maximum life time of single authentication token in seconds (default 7 days)
        """
        self.max_age = max_age
        self.serilizer = URLSafeTimedSerializer(key)

    def generate_auth_token(self, data: str) -> str:
        """
        Generates authentication token for given data

        data: the data to serialize
        """
        return self.serilizer.dumps(data)

    def verify_token(self, token: str) -> Any:
        """
        Verifies authentication token 

        Returns data from token if the token is valid,
        None otherwise

        token: authentication token to verify
        """

        try:
            data = self.serilizer.loads(token, max_age=self.max_age)
            return data
        except BadSignature:
            print('dkjfdk')
            return None
        except SignatureExpired:
            print("sign")
            return None

    def verify_credentials(self, email: str, password: str) -> bool:
        """
        Returns True if email and password are valid,
        False otherwise

        email: email of user
        password: password of user
        """

        user = User.get_by_email(email)
        if not user:
            return False

        return check_password_hash(user.password, password)
