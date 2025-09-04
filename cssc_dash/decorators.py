from functools import wraps
import flask
from flask import request
from .data import get_client
from .tools.jwt_tokens import validate_jwt, get_token_payload

## Return json code for api requests
def auth_required(redirect=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_headers = request.headers.get('Authorization')
            ## For web clients
            if auth_headers:
                token = auth_headers.split()[1]
            else:
                token = request.cookies.get('token')

            if not token:
                if redirect:
                    return flask.redirect(flask.url_for('main.login'))
                return flask.jsonify({"error": f"Bearer token required", "status": 0}), 401

            valid = validate_jwt(token)

            if not valid:
                if redirect:
                    return flask.redirect(flask.url_for('main.logout'))

                return flask.jsonify({"error": f"Bearer Token Invalid", "status": 0}), 401

            token_payload = get_token_payload(token)

            client = get_client(token_payload)

            return f(client, *args, **kwargs)
        return wrapper
    return decorator

