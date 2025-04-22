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


with app.open_resource('static/events.json') as f:
    data = json.load(f)

def load_door_stat():
    with open('static/door_status.json', 'r') as f:
        door_stat = json.load(f)

        return door_stat


def write_door_stat(status):
    with open('static/door_status.json', 'w') as f:
        json.dump({"door_open": status}, f)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    _pass = request.form.get('password')

    if _pass == password:
        session['logged_in'] = True
        return flask.redirect(flask.url_for('dashboard'))
    return flask.redirect(flask.url_for('login'))

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

    door_status = load_door_stat()
    if door_status["door_open"]:
        door_stat = "Open"
    else:
        door_stat = "Closed"
    return flask.render_template('dashboard.html', door_status=door_stat)

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

    return flask.jsonify(load_door_stat())

@app.route('/api/open_door')
def open_door():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))

    write_door_stat(1)
    return flask.redirect(flask.url_for('dashboard'))

@app.route('/api/close_door')
def close_door():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))

    write_door_stat(0)
    return flask.redirect(flask.url_for('dashboard'))