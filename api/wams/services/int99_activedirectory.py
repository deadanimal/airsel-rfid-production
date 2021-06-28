import datetime
import hashlib
import requests
import pytz
import time

from time import gmtime, strftime


def get_active_directory(username, password):

    time_ = str(int(time.time()))

    timezone_ = pytz.timezone('Asia/Kuala_Lumpur')
    time_ = str(int(datetime.datetime.now(timezone_).timestamp()))

    public_key = "9pjCj7PMDLZx7NaD"
    private_key = "ZSMmaAkpQU9y27XWmUYRVbKnyVefV8cg"

    before_sha1 = public_key+username+password+time_+private_key
    after_sha1 = hashlib.sha1(before_sha1.encode())

    request = {
        "key": public_key,
        "username": username,
        "password": password,
        "time": time_,
        "hash": after_sha1.hexdigest()
    }

    response = requests.post(
        "https://api4.airselangor.com/apimgr/api/2/Authenticate", data=request)

    return response.json()
