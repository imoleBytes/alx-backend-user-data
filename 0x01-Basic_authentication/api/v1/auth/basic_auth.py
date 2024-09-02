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
        return authorization_header.removeprefix('Basic ')

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
