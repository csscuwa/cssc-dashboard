import cssc_dash.data.door
from cssc_dash.data import _get_db
from cssc_dash.data.setup import *


db = _get_db()
# db.cursor.execute("""
#            INSERT INTO KeyedData (key, value)
#            VALUES (?, ?)
#    """, ("door_text", "Null"))
#
# db.cursor.execute("""
#            INSERT INTO KeyedData (key, value)
#            VALUES (?, ?)

token = generate_setup_token(db)

print("CSSC: User Manager")


print(f"Their setup token is: http://127.0.0.1:5000/setup?token={token}")

setup_codes = get_setup_codes(db)
print("Current setup codes:")
print(setup_codes)


db.close()