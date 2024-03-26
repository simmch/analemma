from datetime import datetime
import pytz

def get_timestamp():
    # Get the current time in UTC
    now_utc = datetime.now(pytz.utc)

    # Convert it to PST
    now_pst = now_utc.astimezone(pytz.timezone('America/Los_Angeles'))
    return now_pst