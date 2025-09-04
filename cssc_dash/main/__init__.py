import flask

main = flask.Blueprint('main', __name__)

from . import home
from . import finance
from . import login
from . import setup


@main.route('/')
def _index():
    return flask.render_template("index.html")

