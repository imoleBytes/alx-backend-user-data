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


def _generate_uuid() -> str:
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

    def create_session(self, email: str) -> str:
        """
        It takes an email string argument and returns the
        session ID as a string.
        """

        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            self._db._session.commit()

            return user.session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """gets the User object from the session id otherwise return None"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id) -> None:
        """ update user's session id to None """
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ generate reset token and saves to the user and return it"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """ updates the password fiels of the user """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed = _hash_password(password).decode()
        self._db.update_user(user.id, hashed_password=hashed, reset_token=None)


# if __name__ == "__main__":
#     print(_hash_password("Hello Holberton"))
