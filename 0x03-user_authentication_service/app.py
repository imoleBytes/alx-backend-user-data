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
def logout() -> str:
    """ this removes session id from the user's table"""
    token = request.cookies.get("session_id")
    if not token:
        abort(403)
    user = AUTH.get_user_from_session_id(token)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """ handle profile route """
    token = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(token)
    if user:
        return jsonify({"email": f"{user.email}"})
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """ respond to the POST /reset_password route. """
    email = request.form.get("email")

    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify(
            {
                "email": email,
                "reset_token": token
            }
        )
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """ resets user's password """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
