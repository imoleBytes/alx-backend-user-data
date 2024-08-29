#!/usr/bin/env python3
"""
Write a function called filter_datum that returns the log message obfuscated:

Arguments:
fields: a list of strings representing all fields to obfuscate
redaction: a string representing by what the field will be obfuscated
message: a string representing the log line
separator: a string representing by which character is separating all fields
 in the log line (message)
The function should use a regex to replace occurrences of certain field
 values.
filter_datum should be less than 5 lines long and use re.sub to perform
the substitution with a single regex.
"""
import re
import logging
from typing import List
import mysql.connector as MYSQLDB
import os


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated:"""
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        filter_datum(self.fields, self.REDACTION, record, self.SEPARATOR)

        # NotImplementedError
        return ''


def get_db() -> MYSQLDB.connection.MySQLConnection:
    """return a mysql connection """
    conn = MYSQLDB.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return conn


if __name__ == "__main__":

    fields = ["password", "date_of_birth"]
    # fields = ["password", "name"]

    messages = \
        [
            "name=egg;email=eggmin@eggsample.com;\
password=eggcellent;date_of_birth=12/12/1986;",
            "name=bob;email=bob@dylan.com;password=bobbycool;\
date_of_birth=03/04/1993;"
        ]

    for message in messages:
        print(filter_datum(fields, 'xxx', message, ';'))
