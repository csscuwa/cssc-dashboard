from . import main

import flask
from flask import session

from ..decorators import auth_required


@main.route('/finance')
@auth_required(redirect=True)
def finance(client):


    return flask.render_template('finance/index.html')