#!/usr/bin/env python3
"""
In this task, you will set up a basic Flask app.

Create a Flask app that has a single GET route ("/") and use flask.jsonify
to return a JSON payload of the form:
"""
from flask import Flask, jsonify, request, abort, make_response

from auth import Auth


AUTH = Auth()


app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """ the index route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """ users view"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{email}", "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)

    response = make_response(
        jsonify({"email": "<user email>", "message": "logged in"})
    )
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
