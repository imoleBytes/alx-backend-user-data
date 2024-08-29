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


def filter_datum(fields: list[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated:"""
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


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
