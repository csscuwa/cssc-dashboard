from . import Database

import datetime

## DOOR STATUS - OPEN/CLOSED, TEXT

def set_door_status(db: Database, door_status: int, username):
    timestamp = datetime.datetime.now()

    # Set door status to whatever this says it is
    db.cursor.execute("""
        UPDATE KeyedData 
        SET value = ?
        WHERE key = "door_status"
    """, (door_status,))

    # Log this event to door.html log
    db.cursor.execute("""
        INSERT INTO DoorLog (door_status, timestamp, username) 
        VALUES (?, ?, ?);
    """, (door_status, timestamp, username))

def set_door_text(db, door_text: str, user_id: int):
    timestamp = datetime.datetime.now().timestamp()

    # Set door text  to whatever this says it is
    db.cursor.execute("""
            UPDATE KeyedData 
            SET value = ?
            WHERE key = "door_text"
    """, (door_text,))

    # Log this event to door log
    db.cursor.execute("""
            INSERT INTO DoorLog (username, door_text, timestamp) 
            VALUES (?, ?, ?);
    """, (user_id, door_text, timestamp))

def get_door_info(db):
    query = """
            SELECT key, value
            FROM KeyedData
            WHERE key IN ('door_status', 'door_text');
        """
    rows = db.cursor.execute(query).fetchall()

    return {key: value for key, value in rows}


## DOOR KEY LOG





