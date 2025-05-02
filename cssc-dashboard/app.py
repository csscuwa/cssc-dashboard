import flask
from flask import Flask, session
from flask import request

import secrets

import os
import json

import dotenv

dotenv.load_dotenv()


app = flask.Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

password = os.getenv('PASSWORD')

# Base file path
base = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
print()


with app.open_resource('static/events.json') as f:
    data = json.load(f)

def load_door_status():
    with open(f'{base}static/door_status.json', 'r') as f:
        _data = json.load(f)
        return _data


def write_door_status(_data):
    with open(f'{base}/static/door_status.json', 'w') as f:
        json.dump(_data, f)

@app.route('/api/auth', methods=['POST'])
def door_auth():
    _pass = request.form.get('password')

    if _pass == password:
        session['logged_in'] = True
        return flask.jsonify({'logged_in': True})
    return flask.jsonify({'logged_in': False})

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))

    door_status = load_door_status()
    if door_status["door_open"]:
        door_stat = "Open"
    else:
        door_stat = "Closed"

    return flask.render_template('dashboard.html', door_status=door_stat, scrolltext=door_status["scrolltext"])

@app.route('/api/get_events')
def get_events():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))

    return flask.jsonify(data)


@app.route('/')
def login():
    if session.get('logged_in'):
        return flask.redirect(flask.url_for('dashboard'))
    return flask.render_template('login.html')

# API

# Door Status
@app.route('/api/door_status')
def get_door_status():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))

    return flask.jsonify(load_door_status())

@app.route('/api/open_door')
def open_door():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))

    _data = load_door_status()
    _data['door_open'] = 1
    write_door_status(_data)
    return flask.redirect(flask.url_for('dashboard'))

@app.route('/api/close_door')
def close_door():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))

    _data = load_door_status()
    _data['door_open'] = 0
    write_door_status(_data)
    return flask.redirect(flask.url_for('dashboard'))

@app.route('/api/scrolltext_update', methods=['POST'])
def scrolltext_update():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))

    new_scrolltext = request.form.get('scrolltext')
    print(new_scrolltext)
    _data = load_door_status()
    _data["scrolltext"] = new_scrolltext
    write_door_status(_data)

    return flask.redirect(flask.url_for('dashboard'))