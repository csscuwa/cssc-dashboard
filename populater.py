from cssc_dash import data
from cssc_dash.data.user import create_user, user_exists
import bcrypt
import getpass

db = data._get_db()

username = input("Username: ")

password = getpass.getpass('Password: ')
confirm_password = getpass.getpass('Confirm password: ')

if not password == confirm_password:
    print("Passwords don't match")
    exit(1)

discord_handle = input("Discord handle: ")

is_admin = bool(input("Is admin? (1/0: "))

print(create_user(db, username, password, discord_handle, is_admin=is_admin))

print(f"Created user: {username}: {user_exists(db, username)}")


db.close()