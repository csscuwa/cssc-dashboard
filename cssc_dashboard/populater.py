from cssc.data import Database
import bcrypt


db = Database()

db.create_tables()


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

db.add_user("blockbuster206", get_hashed_password("123"), "123")

print(db.get_user(username="blockbuster206"))



db.close()