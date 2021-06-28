from datetime import datetime
import pytz

def convert_gmt8_to_utc0(original_datetime):

    original_datetime_str = ''
    # convert to string
    original_datetime_str = str(original_datetime)

    new_datetime_str = ''
    # check if datetime consist of T and +08:00
    if original_datetime_str.find('T') and original_datetime_str.find('+08:00'):
        # format the datetime
        new_datetime_str = original_datetime_str[0:19].replace('T', ' ')
    else:
        new_datetime_str = original_datetime_str

    # Get local timezone
    local_time = pytz.timezone('Asia/Kuala_Lumpur')

    # Convert to naive datetime object
    naive_datetime = datetime.strptime(new_datetime_str, "%Y-%m-%d %H:%M:%S")

    # Update naive datetime object with local timezone
    local_datetime = local_time.localize(naive_datetime, is_dst=None)

    # Convert to UTC
    utc_datetime = local_datetime.astimezone(pytz.utc)

    # Return as ISO
    return utc_datetime.isoformat()