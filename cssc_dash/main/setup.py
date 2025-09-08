import flask
from flask import request, session

from . import main

from ..data import _get_db
from ..data.setup import validate_setup_token, remove_setup_token
from ..data.user import create_user

@main.route("/setup/submit", methods=["POST"])
def setup_submit():
    if not session.get('setupcode'):
        return flask.redirect(flask.url_for("main.login"))

    username = request.form.get('username')
    password = request.form.get('password')
    discord_handle = request.form.get('discord')

    db = _get_db()
    create_user(db, username, password, discord_handle)

    remove_setup_token(db, session['setupcode'])
    db.close()

    session.pop('setupcode')

    response = flask.jsonify({"status": 1, "account_created": True})


    return response

@main.route("/setup")
def validate_setup():
    setuptoken = request.args.get('token')

    if not setuptoken:
        return "Setup token is missing!", 400

    db = _get_db()
    setupcode = validate_setup_token(db, setuptoken)
    db.close()

    if setupcode:
        session['setupcode'] = setupcode
        return flask.redirect(flask.url_for("main.setup_form"))

    return "Setup code invalid!", 401



@main.route("/setup/form")
def setup_form():
    if not session.get('setupcode'):
        return flask.render_template("errors/401.html")

    return flask.render_template("auth/setup.html")
