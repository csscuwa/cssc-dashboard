from flask import request

from ..data import _get_db
from ..data.door import *

import flask

from ..decorators import auth_required

device = flask.Blueprint('device', __name__)


@device.route('/confirm')
def _index():

    return flask.jsonify()