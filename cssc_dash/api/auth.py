from . import api

import flask
from flask import request, session

from ..data import _get_db
from ..tools.jwt_tokens import *
from ..data.user import user_exists, validate_password


@api.route('/auth', methods=["POST"])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    username = username.lower()

    logged_in = False
    token = None

    db = _get_db()

    if user_exists(db, username):
        if validate_password(db, username, password):
            token = get_user_token(username)
            logged_in = True
    db.close()

    response = flask.jsonify({"logged_in": logged_in})
    if token:
        response.set_cookie("token", token, httponly=True, secure=True, samesite='Strict')

    return response, 200