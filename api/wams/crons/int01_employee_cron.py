from datetime import datetime, timedelta
import requests
import pytz


def int01_employee_cron():

    print('int01_employee_cron')

    # get timezone
    timezone_ = pytz.timezone("Asia/Kuala_Lumpur")

    # datetime object containing current date and time
    now = datetime.now(timezone_)

    print("now =", now)

    # dd/mm/YY H:M:S
    from_date = now.strftime("%Y-%m-%dT%H:00:00+00:00")
    to_date = now.strftime("%Y-%m-%dT%H:59:59+00:00")

    print('from_date = ',from_date)
    print('to_date = ',to_date)

    payload = {
        "service_name": "getEmployee"
        # "from_date": from_date,
        # "to_date": to_date
    }

    r = requests.post(
        "https://airsel-rfid-api-prod.pipe.my/v1/wams/services/", json=payload)

    print('status = ',r.status_code)
