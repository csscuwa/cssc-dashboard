from cssc_dash.data import _get_db


db = _get_db()

door_log_delete = """
        DROP TABLE IF EXISTS DoorLog;
"""

db.cursor.execute(door_log_delete)

door_log_table = """
        CREATE TABLE IF NOT EXISTS DoorLog (
            'door_status' INT,
            'door_text' TEXT,
            'timestamp' DATETIME NOT NULL,
            'username' TEXT NOT NULL
        );
    """

db.cursor.execute(door_log_table)