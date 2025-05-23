from datetime import datetime, timedelta

def monday_730(current_week=True):
    # Get today's date
    today = datetime.today()
    if current_week:
        # Calculate the date of this week's Monday
        monday = today - timedelta(days=today.weekday())
    else:
        # Calculate the date of last Monday
        monday = today - timedelta(days=today.weekday() + 7)
    # Combine the date of Monday with the time 07:30
    monday_730 = datetime.combine(monday, datetime.strptime('07:30', '%H:%M').time())
    # Convert datetime to milliseconds
    milliseconds = int(monday_730.timestamp() * 1000)
    return milliseconds

def monday_730_lw(current_week=True):
    # Get today's date
    today = datetime.today()
    if current_week:
        # Calculate the date of this week's Monday
        monday = today - timedelta(days=today.weekday() + 7)
    else:
        # Calculate the date of last Monday
        monday = today - timedelta(days=today.weekday() + 14)
    # Combine the date of Monday with the time 07:30
    monday_730 = datetime.combine(monday, datetime.strptime('07:30', '%H:%M').time())
    # Convert datetime to milliseconds
    milliseconds = int(monday_730.timestamp() * 1000)
    return milliseconds