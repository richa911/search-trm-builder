import webbrowser
from datetime import datetime, timedelta
import time

def open_in_browser(url):
    print(f"🔗 Opening URL: {url}")
    webbrowser.open(url, new=0)

def get_last_week_date_range():
    """
    Returns (start_date, end_date) as datetime objects:
    - Start date: Last week's Monday (00:00:00)
    - End date: This week's Sunday (23:59:59)
    """
    today = datetime.today()
    last_monday = today - timedelta(days=today.weekday() + 7)
    this_sunday = last_monday + timedelta(days=6)
    start_dt = datetime.combine(last_monday.date(), datetime.min.time()) 
    end_dt = datetime.combine(this_sunday.date(), datetime.max.time())    
    return start_dt, end_dt

def to_unix_ms(dt):
    """Converts a datetime to Unix timestamp in milliseconds."""
    return int(time.mktime(dt.timetuple()) * 1000)

def open_grafana_dashboards():
    start_dt, end_dt = get_last_week_date_range()
    from_ts = to_unix_ms(start_dt)
    to_ts = to_unix_ms(end_dt)

    base_urls = [
        "https://eagleeye.swiggyops.de/d/U8gLl2p4z/search-flash-view?orgId=1&viewPanel=516",
        "https://eagleeye.swiggyops.de/d/HycT2J9Wk/voyager-search-service?orgId=1&viewPanel=30",
        "https://eagleeye.swiggyops.de/d/I4KbkYMfH/alfred-suggest-service?orgId=1&viewPanel=30",
        "https://eagleeye.swiggyops.de/d/POg9MU27z/scout?orgId=1&viewPanel=30",
        "https://eagleeye.swiggyops.de/d/137nEitSk/conan-discovery-service?orgId=1&viewPanel=84"
    ]

    for base_url in base_urls:
        full_url = f"{base_url}&from={from_ts}&to={to_ts}"
        open_in_browser(full_url)


def open_cost_explorer_chart():
    today = datetime.today()
    last_monday = today - timedelta(days=today.weekday() + 7)
    this_sunday = last_monday + timedelta(days=6)

    # Format dates
    start_date_str = last_monday.strftime('%Y-%m-%d')
    end_date_str = this_sunday.strftime('%Y-%m-%d')

    url_template = (
        "https://us-east-1.console.aws.amazon.com/costmanagement/home?region=ap-south-1#/cost-explorer?"
        "chartStyle=STACK&costAggregate=netAmortizedCost&endDate={end_date}&excludeForecasting=false&"
        "filter=%5B%7B%22dimension%22:%7B%22id%22:%22RecordTypeV2%22,%22displayValue%22:%22Charge%20type%22%7D,"
        "%22operator%22:%22INCLUDES%22,%22values%22:%5B%7B%22value%22:%22Usage%22,%22displayValue%22:%22Usage%22%7D,"
        "%7B%22value%22:%22SavingsPlanCoveredUsage%22,%22displayValue%22:%22Savings%20Plan%20Covered%20Usage%22%7D,"
        "%7B%22value%22:%22DiscountedUsage%22,%22displayValue%22:%22Reservation%20applied%20usage%22%7D%5D%7D,"
        "%7B%22dimension%22:%7B%22id%22:%22TagKey%22,%22displayValue%22:%22Tag%22%7D,%22operator%22:%22INCLUDES%22,"
        "%22values%22:%5B%7B%22value%22:%22search%22,%22displayValue%22:%22search%22%7D%5D,%22growableValue%22:"
        "%7B%22value%22:%22pod%22,%22displayValue%22:%22pod%22%7D%7D%5D&futureRelativeRange=CUSTOM&granularity=Daily&"
        "groupBy=%5B%22Service%22%5D&historicalRelativeRange=CUSTOM&isDefault=false&reportArn=arn:aws:ce::361474736119:"
        "ce-saved-report%2F9c748a47-367b-4448-a867-c4c438ad98d5&reportId=9c748a47-367b-4448-a867-c4c438ad98d5&"
        "reportName=SF-Search%20Overall%20Cost%20Report&showOnlyUncategorized=false&showOnlyUntagged=false&"
        "startDate={start_date}&usageAggregate=undefined&useNormalizedUnits=false"
    )

    # Fill in the dates
    full_url = url_template.format(start_date=start_date_str, end_date=end_date_str)
    open_in_browser(full_url)
