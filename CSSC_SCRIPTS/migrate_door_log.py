from cssc_dash.data import _get_db


db = _get_db()

# Create record if not exists
db.cursor.execute("""
            INSERT INTO KeyedData (key, value)
            VALUES (?, ?);
    """, ("door_last_ping", "null"))
