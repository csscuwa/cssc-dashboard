import datetime
from functools import wraps
from reprlib import recursive_repr

import flask
from flask import session, request

import os

import dotenv

from cssc.data import _get_db

dotenv.load_dotenv()

app = flask.Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

from cssc.authentication import auth

app.register_blueprint(auth)


password = os.getenv('PASSWORD')

# Base file path
base = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]


def is_authenticated():
    logged_in = session.get('logged_in')
    return logged_in

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            return flask.redirect(flask.url_for('login'))
        return f(*args, **kwargs)
    return wrapper

@app.route('/')
def login():
    if is_authenticated():
        return flask.redirect(flask.url_for('dashboard'))
    return flask.render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session.get('user_id')
    db = _get_db()
    info = db.get_door_info()
    user_data = db.get_user(user_id=user_id)
    db.close()

    if int(info["door_status"]):
        door_status = "Open"
    else:
        door_status = "Closed"

    return flask.render_template('dashboard.html', username=user_data["username"], door_status=door_status, scrolltext=info["door_text"])


# # API
#
# Door Status
@app.route('/api/door_status')
def get_door_status():
    db = _get_db()
    info = db.get_door_info()
    db.close()

    return flask.jsonify(info)

#
@app.route('/api/open_door')
@login_required
def open_door():
    user_id = session.get('user_id')
    db = _get_db()
    db.update_door_status(1, user_id)
    db.close()

    return flask.redirect(flask.url_for('dashboard'))

@app.route('/api/close_door')
@login_required
def close_door():
    user_id = session.get('user_id')
    db = _get_db()
    db.update_door_status(0, user_id)
    db.close()

    return flask.redirect(flask.url_for('dashboard'))

@app.route('/api/door_log')
@login_required
def get_door_log():
    db = _get_db()
    raw_data = db.get_door_log()
    door_log = []

    print(raw_data)

    for record in raw_data:
        print(record)
        user_info = db.get_user(user_id=record[0])
        door_log.append({
            "username": user_info["username"],
            "door_status": record[1],
            "door_text": record[2],
            "timestamp": record[3],
            "time": datetime.datetime.fromtimestamp(record[3]).isoformat()
        })

    db.close()

    return door_log

#
@app.route('/api/scrolltext_update', methods=['POST'])
@login_required
def scrolltext_update():
    new_scrolltext = request.form.get('scrolltext')

    user_id = session.get('user_id')
    db = _get_db()
    db.update_door_text(new_scrolltext, user_id)
    db.close()

    return flask.redirect(flask.url_for('dashboard'))