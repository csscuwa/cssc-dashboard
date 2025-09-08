import cssc_dash.data.door
from cssc_dash.data import _get_db

db = _get_db()

print(cssc_dash.data.door.get_latest_door_log(db))