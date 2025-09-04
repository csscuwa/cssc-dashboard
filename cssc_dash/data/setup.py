import secrets
import string

from ..tools.jwt_tokens import *

# Setup new users

def generate_setup_token(db):
    setup_code = ''.join(secrets.choice(string.digits) for _ in range(6))

    setup_payload = {"type": "setup", "code": setup_code}
    token = encode_jwt(setup_payload)

    db.cursor.execute("INSERT into SetupCodes(code) VALUES (?)", (setup_code,))

    return token

def validate_setup_token(db, token):
    validated = validate_jwt(token)

    if not validated:
        return False

    payload = get_token_payload(token)

    setup_code = payload["code"]

    db.cursor.execute("SELECT EXISTS (SELECT 1 FROM SetupCodes WHERE code = ?);", (setup_code,))
    if bool(db.cursor.fetchone()[0]):
        return setup_code
    else:
        return False


def get_setup_codes(db):
    result = db.cursor.execute("SELECT code FROM SetupCodes")
    return result.fetchall()

def remove_setup_token(db, code):

    db.cursor.execute("DELETE FROM SetupCodes WHERE code = ?;", (code,))