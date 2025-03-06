import flask
from flask import Flask, session
from flask import request

import secrets

import os

import dotenv

dotenv.load_dotenv()




app = flask.Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

password = os.getenv('PASSWORD')

@app.route('/authenticate', methods=['POST'])
def hellp_world():
    data = request.form.get('password')

    if data == password:
        session['logged_in'] = True
        return flask.redirect(flask.url_for('dashboard'))
    return flask.redirect(flask.url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('login'))
    return flask.render_template('dashboard.html')

@app.route('/')
def login():
    if session.get('logged_in'):
        return flask.redirect(flask.url_for('dashboard'))
    return flask.render_template('index.html')