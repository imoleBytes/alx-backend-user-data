#!/usr/bin/env python3
"""
In this task you will define a _hash_password method that takes in a password
string arguments and returns bytes.

The returned bytes is a salted hash of the input password, hashed with bcrypt.
hashpw.
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ hash password and return the hashed bytes"""
    salt = bcrypt.gensalt()

    hashed_pass = bcrypt.hashpw(password.encode(), salt)
    return hashed_pass


def _generate_uuid():
    """ generate UUID string """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """ initialize AUth"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        this handle user registration
        """
        if email is None or password is None:
            # return None
            raise ValueError(f"email and password are mandatory")

        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pass = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pass.decode())
            return new_user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """ checks if user is valid """
        if email is None or password is None:
            return False

        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False

        return bcrypt.checkpw(
            password.encode(), str(user.hashed_password).encode()
        )


# if __name__ == "__main__":
#     print(_hash_password("Hello Holberton"))
