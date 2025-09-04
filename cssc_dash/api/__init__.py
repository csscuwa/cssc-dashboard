import flask

api = flask.Blueprint('api', __name__)

from . import auth, door

from .door import door as door_blueprint
from .device import device as device_blueprint

api.register_blueprint(door_blueprint, url_prefix='/door')
api.register_blueprint(device_blueprint, url_prefix='/device')
