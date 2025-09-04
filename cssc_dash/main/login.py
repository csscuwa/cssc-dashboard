import flask
from flask import session, request, make_response

from ..decorators import auth_required

from . import main


@main.route('/login')
def login():
    return flask.render_template('auth/login.html')

@main.route('/logout')
@auth_required(redirect=True)
def logout(client):
    response = make_response(flask.redirect(flask.url_for('.login')))
    response.delete_cookie("token")

    return response