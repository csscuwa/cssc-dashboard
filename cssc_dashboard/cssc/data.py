import sqlite3
import bcrypt

import datetime


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)

import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # Creating tables

        users_table = """
            CREATE TABLE IF NOT EXISTS Users (
                'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'username' TEXT UNIQUE NOT NULL,
                'password' TEXT NOT NULL,
                'discord_handle' TEXT NOT NULL
            );
        """

        self.cursor.execute(users_table)

        # Door Status: Whether it is open or not.
        # Door Text: What the scrolling text is set to.

        door_log_table = """
            CREATE TABLE IF NOT EXISTS DoorLog (
                'user_id' INT NOT NULL,
                'door_status' INT,
                'door_text' TEXT,
                'timestamp' INT NOT NULL
            );
        """

        self.cursor.execute(door_log_table)

        keyed_data_table = """
            CREATE TABLE IF NOT EXISTS KeyedData (
                key TEXT NOT NULL UNIQUE PRIMARY KEY,
                value TEXT NOT NULL
            );
        """

        self.cursor.execute(keyed_data_table)

        # Create records if they dont exists
        try:
            self.cursor.execute("""
                INSERT INTO KeyedData (key, value)
                VALUES (?, ?);
            """, ("door_status", "0"))

            # Create record if not exists
            self.cursor.execute("""
                INSERT INTO KeyedData (key, value)
                VALUES (?, ?);
            """, ("door_text", "Hi"))
        except:
            pass

    def update_door_status(self, door_status: int, user_id: int):
        timestamp = datetime.datetime.now().timestamp()

        # Set door to whatever this says it is
        self.cursor.execute("""
            UPDATE KeyedData 
            SET value = ?
            WHERE key = "door_status"
        """, (door_status,))

        # Log this event to door log
        self.cursor.execute("""
            INSERT INTO DoorLog (user_id, door_status, timestamp) 
            VALUES (?, ?, ?);
        """, (user_id, door_status, timestamp))

    def update_door_text(self, door_text: str, user_id: int):
        timestamp = datetime.datetime.now().timestamp()

        # Set door to whatever this says it is
        self.cursor.execute("""
               UPDATE KeyedData 
               SET value = ?
               WHERE key = "door_text"
           """, (door_text,))

        # Log this event to door log
        self.cursor.execute("""
               INSERT INTO DoorLog (user_id, door_text, timestamp) 
               VALUES (?, ?, ?);
           """, (user_id, door_text, timestamp))

    # Returns door open status and text
    def get_door_info(self):
        door_info = self.cursor.execute("""
            SELECT *
            FROM KeyedData
            WHERE key = "door_status" or key = "door_text";
        """).fetchmany(2)

        return {
            door_info[0][0]: door_info[0][1],
            door_info[1][0]: door_info[1][1]
        }


    def get_door_log(self):
        door_log = self.cursor.execute("""
            SELECT *
            FROM DoorLog;
        """).fetchall()

        return door_log

    def add_user(self, username, hashed_password, discord_handle):
        self.cursor.execute("INSERT INTO Users(username, password, discord_handle) VALUES (?, ?, ?)", (username, hashed_password, discord_handle))

    def get_user(self, username=None, user_id=None):
        results = self.cursor.execute("SELECT * FROM Users WHERE username = ? or id = ?", (username, user_id))
        result = results.fetchone()

        if not result:
            return None

        return {
            'id': result[0],
            'username': result[1],
            'password': result[2],
            'discord_handle': result[3]
        }

    def close(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

def _get_db():
    db = Database()
    db.create_tables()
    return db
