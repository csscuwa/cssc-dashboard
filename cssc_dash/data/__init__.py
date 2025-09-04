import sqlite3
import jwt
import os

from .user import get_user_data




class Database:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()


### setup_user

class Client:
    def __init__(self, _token_payload):
        self.username = _token_payload["username"]
        self.type = _token_payload["type"]


class User(Client):
    def __init__(self, _token_payload,  user_data):
        super().__init__(_token_payload)
        self.discord_handle = user_data["discord_handle"]


def _get_db():
    return Database()

# Get client information

def get_client(token_payload):
    if token_payload["type"] == "user":
        db = _get_db()
        user_data = get_user_data(db, token_payload["username"])
        db.close()

        client = User(token_payload, user_data)
        return client
    else:
        return None
