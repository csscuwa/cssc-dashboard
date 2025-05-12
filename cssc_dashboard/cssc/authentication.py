import flask
from flask import request, session
import bcrypt

from cssc.data import _get_db


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)


auth = flask.Blueprint('auth', __name__, url_prefix='/auth')
admin = flask.Blueprint('admin', __name__, url_prefix='/admin')


@auth.route('/', methods=['POST'])
def _index():
    db = _get_db()
    username = request.form.get('username')
    password = request.form.get('password')

    print(username, password)


    user_data = db.get_user(username=username)

    db.close()

    if not user_data:
        return flask.jsonify({'logged_in': False})

    if check_password(password, user_data['password']):
        session['logged_in'] = True
        session['user_id'] = user_data['id']
        return flask.jsonify({'logged_in': True})
    return flask.jsonify({'logged_in': False})







