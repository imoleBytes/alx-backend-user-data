#!/usr/bin/env python3
"""
In this task you will define a _hash_password method that takes in a password
string arguments and returns bytes.

The returned bytes is a salted hash of the input password, hashed with bcrypt.
hashpw.
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ hash password and return the hashed bytes"""
    salt = bcrypt.gensalt()

    hashed_pass = bcrypt.hashpw(password.encode(), salt)
    return hashed_pass


if __name__ == "__main__":
    print(_hash_password("Hello Holberton"))
