from datetime import datetime, timedelta

user_last_sent = {}

def is_rate_limited(user_id):
    now = datetime.now()
    if user_id in user_last_sent and now - user_last_sent[user_id] < timedelta(seconds=15):
        return True
    user_last_sent[user_id] = now
    return False
