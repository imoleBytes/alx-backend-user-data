#!/usr/bin/env python3
"""
User passwords should NEVER be stored in plain text in a database.
Implement a hash_password function that expects one string argument
name password and returns a salted, hashed password, which is a byte string.
Use the bcrypt package to perform the hashing (with hashpw).
"""
import bcrypt


def hash_password(password: str) -> str:
    """ hash pasword """
    bytes_password = password.encode()

    hashed_pwd = bcrypt.hashpw(bytes_password, bcrypt.gensalt())
    return hashed_pwd


if __name__ == "__main__":
    password = "MyAmazingPassw0rd"
    print(hash_password(password))
    print(hash_password(password))
