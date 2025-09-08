from flask import request

from ..data import _get_db
from ..data.door import *

import flask

from ..decorators import auth_required

device = flask.Blueprint('device', __name__)

@auth_required(bot=True)
@device.route('/confirm')
def _index():
    confirm_token = request.args.get('token')


    return flask.jsonify()