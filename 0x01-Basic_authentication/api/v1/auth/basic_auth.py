#!/usr/bin/env python3
"""
Create a class BasicAuth that inherits from Auth. For the moment
 this class will be empty.
Update api/v1/app.py for using BasicAuth class instead of Auth
 depending of the value of the environment variable AUTH_TYPE,
 If AUTH_TYPE is equal to basic_auth:

import BasicAuth from api.v1.auth.basic_auth
create an instance of BasicAuth and assign it to the variable auth
Otherwise, keep the previous mechanism with auth an instance of Auth.

In the first terminal:
"""
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ basic auth implementation"""
    def extract_base64_authorization_header(self, authorization_header: str)\
            -> str:
        """ this extract the string after 'Basic ' """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[-1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ decode base64 str """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str)\
            -> (str, str):
        """ extract user credentials """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        splitted_str = decoded_base64_authorization_header.split(':')
        email = splitted_str[0]
        passwd = decoded_base64_authorization_header.removeprefix(email)
        passwd = passwd[1:]

        return email, passwd

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """eturns the User instance based on his email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns a User instance based on the received request"""
        auth_header = self.authorization_header(request)
        if auth_header:
            token = self.extract_base64_authorization_header(auth_header)
            if token:
                decoded_token = self.decode_base64_authorization_header(token)
                if decoded_token:
                    email, pwd = self.extract_user_credentials(decoded_token)
                    if email:
                        return self.user_object_from_credentials(email, pwd)
        return None
