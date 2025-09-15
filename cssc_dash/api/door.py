from flask import request

from ..data import _get_db
from ..data.door import *

import flask

from ..decorators import auth_required

door = flask.Blueprint('door', __name__)


@door.route('/')
def _index():
    db = _get_db()
    info = get_door_info(db)
    db.close()

    return flask.jsonify(info)

@door.route('/ping')
@auth_required(bot=True)
def ping(client):
    db = _get_db()
    info = get_door_info(db)
    set_last_ping(db)
    db.close()

    return flask.jsonify(info)

@door.route('/latest_log')
def latest_log():
    db = _get_db()
    info = get_latest_door_log(db)
    db.close()

    return flask.jsonify(info)



@door.route('/set_text', methods=['POST'])
@auth_required()
def _set_text(client):
    new_door_text = request.form.get('door_text')

    db = _get_db()
    set_door_text(db, new_door_text, client.username)
    db.close()

    return flask.jsonify({"status": 1}), 200

@door.route('/open')
@auth_required()
def _open(client):
    db = _get_db()
    set_door_status(db, 1, client.username)
    db.close()

    return flask.jsonify({"status": 1}), 200

@door.route('/close')
@auth_required()
def _close(client):
    db = _get_db()
    set_door_status(db, 0, client.username)
    db.close()

    return flask.jsonify({"status": 1}), 200
