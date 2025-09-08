from . import main

import flask
from flask import session

from ..decorators import auth_required

from ..data import _get_db
from ..data.door import get_door_info


@main.route('/home')
@auth_required(redirect=True)
def home(client):
    db = _get_db()
    door_info = get_door_info(db)
    door_text = door_info['door_text']

    db.close()

    return flask.render_template('home.html', username=client.username, door_text=door_text)