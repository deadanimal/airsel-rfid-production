from datetime import datetime, timedelta
import requests
import pytz


def int09_measurementtype_cron():

    print('int09_measurementtype_cron')

    # get timezone
    timezone_ = pytz.timezone("Asia/Kuala_Lumpur")

    # datetime object containing current date and time
    now = datetime.now(timezone_)

    print("now =", now)

    # dd/mm/YY H:M:S
    from_date = now.strftime("%Y-%m-%dT%H:25:00+00:00")
    to_date = (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:24:59+00:00")

    payload = {
        "service_name": "getMeasurementType"
    }

    r = requests.post(
        "https://airsel-rfid-api-prod.pipe.my/v1/wams/services/", json=payload)
