#!/usr/bin/env python3
""" Now you will create a class to manage the API authentication.
Create a folder api/v1/auth
Create an empty file api/v1/auth/__init__.py
Create the class Auth:
in the file api/v1/auth/auth.py
import request from flask
class name Auth
public method def require_auth(self, path: str, excluded_paths: List[str])
 -> bool: that returns False - path and excluded_paths will be used later,
 now, you don't need to take care of them
public method def authorization_header(self, request=None) -> str: that
returns None - request will be the Flask request object
public method def current_user(self, request=None) -> TypeVar('User'):
 that returns None - request will be the Flask request object
This class is the template for all authentication system you will implement.
"""
# from flask import request
from typing import (List, TypeVar)


class Auth:
    """ This is the Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ public require_auth method
            Return bool
        """
        if path and path[-1] != '/':
            path += '/'

        if excluded_paths is None or '':
            return True
        if path is None or path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ authorization header method"""
        if request is None:
            return None
        if 'Authorization' in request.headers:
            return request.headers.get('Authorization')
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User') | None:
        """ return user or none"""
        return None
