#!/usr/bin/env python3
"""
In this task, you will set up a basic Flask app.

Create a Flask app that has a single GET route ("/") and use flask.jsonify
to return a JSON payload of the form:
"""
from flask import Flask, jsonify, request, abort, make_response, redirect

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
    """ create login session """
    try:
        email = request.form.get("email")
        password = request.form.get("password")
    except Exception:
        email = None
        password = None

    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)

    response = make_response(
        jsonify({"email": "<user email>", "message": "logged in"})
    )
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """ this removes session id from the user's table"""
    token = request.cookies.get("session_id")
    if not token:
        abort(403)
    user = AUTH.get_user_from_session_id(token)
    if user:
        AUTH.destroy_session(user.id)
        redirect("/")
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
