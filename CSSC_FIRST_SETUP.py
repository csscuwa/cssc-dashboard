from cssc_dash.data import _get_db

### SQL SCHEME
"""
User 

Door_log

KeyedData - for key - data

SetupCodes - For setups


"""

def create_tables(cursor):
    # Creating tables

    users_table = """
        CREATE TABLE IF NOT EXISTS Users (
            'username' TEXT NOT NULL UNIQUE PRIMARY KEY,
            'hashed_password' TEXT NOT NULL,
            'discord_handle' TEXT NOT NULL
        );
    """

    cursor.execute(users_table)

    # Door Status: Whether it is open or not.
    # Door Text: What the scrolling text is set to.

    door_log_table = """
        CREATE TABLE IF NOT EXISTS DoorLog (
            'door_status' INT,
            'door_text' TEXT,
            'timestamp' INT NOT NULL,
            'username' TEXT NOT NULL
        );
    """

    cursor.execute(door_log_table)

    keyed_data_table = """
        CREATE TABLE IF NOT EXISTS KeyedData (
            key TEXT NOT NULL UNIQUE PRIMARY KEY,
            value TEXT NOT NULL
        );
    """

    cursor.execute(keyed_data_table)

    setup_codes_table = """
        CREATE TABLE IF NOT EXISTS SetupCodes (
            code TEXT NOT NULL UNIQUE PRIMARY KEY
        );
    """

    cursor.execute(setup_codes_table)

    # Create records if they dont exists
    cursor.execute("""
        INSERT INTO KeyedData (key, value)
        VALUES (?, ?);
    """, ("door_status", "0"))
    # Create record if not exists
    cursor.execute("""
            INSERT INTO KeyedData (key, value)
            VALUES (?, ?);
    """, ("door_text", "Hello, CSSC cool!"))

db = _get_db()
print("Creating tables..")
create_tables(db.cursor)

db.close()
# Set door text  to whatever this says it is

# db.cursor.execute("""
#            INSERT INTO KeyedData (key, value)
#            VALUES (?, ?)
#    """, ("door_text", "Null"))
#
# db.cursor.execute("""
#            INSERT INTO KeyedData (key, value)
#            VALUES (?, ?)
#         """, ("door_status", "0"))


