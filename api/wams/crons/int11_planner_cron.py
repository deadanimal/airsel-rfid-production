from datetime import datetime, timedelta
import requests
import pytz


def int11_planner_cron():

    print('int11_planner_cron')

    # get timezone
    timezone_ = pytz.timezone("Asia/Kuala_Lumpur")

    # datetime object containing current date and time
    now = datetime.now(timezone_)

    print("now =", now)

    # dd/mm/YY H:M:S
    from_date = now.strftime("%Y-%m-%dT%H:30:00+00:00")
    to_date = (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:29:59+00:00")

    payload = {
        "service_name": "getPlanner"
        # "from_date": from_date,
        # "to_date": to_date
    }

    r = requests.post(
        "https://airsel-rfid-api-prod.pipe.my/v1/wams/services/", json=payload)
