import jwt
import os


SECRET_KEY = os.getenv('SECRET_KEY')

def get_token_payload(token):
    return jwt.decode(token, options={"verify_signature": False})

def encode_jwt(payload):
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def get_user_token(username):
    user_token = jwt.encode({"type": "user", "username": username}, SECRET_KEY, algorithm="HS256")
    return user_token

def get_bot_token(bot_name):
    bot_token = jwt.encode({"type": "bot", "name": bot_name}, SECRET_KEY, algorithm="HS256")
    return bot_token

def validate_jwt(token):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])  # Replace 'HS256' with the actual algorithm
        return True
    except Exception as e:
        print(e)
        return None