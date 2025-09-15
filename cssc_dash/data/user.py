from ..tools.jwt_tokens import *

import secrets
import string

import bcrypt

### User Password Authorization

def generate_hashed_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def get_hashed_password(db, username):
    result = db.cursor.execute("SELECT hashed_password FROM Users WHERE username = ?;", (username,))
    return result.fetchone()[0]

### Password validation

def validate_password(db, username, password):
    hashed_password = get_hashed_password(db, username)

    if not hashed_password:
        return

    return bcrypt.checkpw(password.encode(), hashed_password)

def change_password(db, username, old_password, new_password):
    password = generate_hashed_password(new_password)


# Check users

def user_exists(db, username):
    result = db.cursor.execute("SELECT EXISTS (SELECT 1 FROM Users WHERE username = ?);", (username,))
    return bool(result.fetchone()[0])

def get_user_data(db, username):
    if not user_exists(db, username):
        return None

    result = db.cursor.execute("SELECT * FROM Users WHERE username = ?;", (username,))
    user_data = result.fetchone()

    return {
        "username": user_data[0],
        "discord_handle": user_data[1],
        "admin": user_data[2],
    }


def create_user(db, username, password, discord_handle):
    username = username.lower()
    hashed_password = generate_hashed_password(password)
    db.cursor.execute("INSERT INTO Users(username, hashed_password, discord_handle) VALUES (?, ?, ?);",
                        (username, hashed_password, discord_handle))