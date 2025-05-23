import opsgenie_sdk
from decouple import config as configEnv
from util import monday_730, monday_730_lw
from html_helper import create_html_table_row
import html_helper
import pytz
from collections import Counter

# Opsgenie API key
OPS_GENIE_API_KEY = 'OPS_GENIE_API_KEY'
# URL for the incident details
INCIDENT_URL = 'https://bundltechnologies.app.opsgenie.com/alert/detail/'
# Placeholder for the description in the HTML table
DESCRIPTION_PLACEHOLDER = (
    "<p><i><u>What</u></i>: </p>"
    "<p><i><u>Why</u></i>: </p>"
    "<p><i><u>Impact</u></i>: </p>"
    "<p><i><u>AI</u></i>: </p>"
)


def list_alerts(team, priority='P1'):
    """
    This function lists all the alerts from Opsgenie.
    """
    conf = opsgenie_sdk.configuration.Configuration()
    conf.api_key['Authorization'] = configEnv(OPS_GENIE_API_KEY)
    conf.verify_ssl = False

    alert_api = opsgenie_sdk.AlertApi(api_client=opsgenie_sdk.api_client.ApiClient(configuration=conf))
    query = 'teams: "{}" AND priority: {} AND createdAt > {} AND createdAt < {}'.format(team, priority,
                                                                                        monday_730(current_week=False),
                                                                                        monday_730(current_week=True))

    try:
        alerts = []
        offset = 0
        limit = 100

        while True:
            response = alert_api.list_alerts(limit=limit, sort='createdAt', order='asc', query=query, offset=offset)
            alerts.extend(response.data)

            if len(response.data) < limit:
                break
            offset += limit
        return alerts
    except opsgenie_sdk.rest.ApiException as err:
        print("Exception when calling AlertApi->list_alerts: {}".format(err))


def list_alerts_lw(team, priority='P1'):
    """
    This function lists all the alerts from Opsgenie.
    """
    conf = opsgenie_sdk.configuration.Configuration()
    conf.api_key['Authorization'] = configEnv(OPS_GENIE_API_KEY)
    conf.verify_ssl = False

    alert_api = opsgenie_sdk.AlertApi(api_client=opsgenie_sdk.api_client.ApiClient(configuration=conf))
    query = 'teams: "{}" AND priority: {} AND createdAt > {} AND createdAt < {}'.format(team, priority,
                                                                                        monday_730_lw(current_week=False),
                                                                                        monday_730_lw(current_week=True))

    try:
        alerts = []
        offset = 0
        limit = 100

        while True:
            response = alert_api.list_alerts(limit=limit, sort='createdAt', order='asc', query=query, offset=offset)
            alerts.extend(response.data)

            if len(response.data) < limit:
                break
            offset += limit
        return alerts
    except opsgenie_sdk.rest.ApiException as err:
        print("Exception when calling AlertApi->list_alerts: {}".format(err))


def convert_resp_to_table(alerts, title, last_week_alerts=None):
    rows = {}
    incident_rows = [create_html_table_row("th", [
        "S.No.", "Date(s)", "Incident", "Count", "Last Week Count", "Description", "Internal/External"
    ])]
    s_no = 0

    # Normalize last_week_alerts as just a list of strings (incident messages)
    last_week_msgs = []
    if last_week_alerts:
        for alert in last_week_alerts:
            if hasattr(alert, 'message'):
                last_week_msgs.append(alert.message.strip().lower())
            else:
                last_week_msgs.append(str(alert).strip().lower())

    for i in alerts:
        incident = i.message.replace("<", "less than").replace(">", "greater than")
        date_time = i.created_at.astimezone(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%Y %I:%M %p")
        date_time_hyperlink = INCIDENT_URL + i.id

        if incident not in rows:
            rows[incident] = {"date_time": [], "count": 0}

        rows[incident]["date_time"].append(
            f'<a href = "{date_time_hyperlink}" target="_blank">{date_time}</a>'
        )
        rows[incident]["count"] += 1

    for incident in rows:
        s_no += 1
        normalized_incident = incident.strip().lower()
        last_week_count = last_week_msgs.count(normalized_incident)

        row = create_html_table_row("td", [
            s_no,
            "<br/>".join(rows[incident]["date_time"]),
            incident,
            rows[incident]["count"],
            last_week_count,
            DESCRIPTION_PLACEHOLDER,
            ""
        ])
        incident_rows.append(row)

    return html_helper.add_title(title, 2) + """
        <table style="width: 100%; border-collapse: collapse;">
            {}</table><br/>
    """.format("".join(incident_rows))



def convert_resp_to_analytics_table(alerts, top_n=5):
    """
    This function converts the response from the Opsgenie API to an HTML analytics table.
    """
    rows = {}
    incident_counter = Counter()

    for i in alerts:
        incident = i.message.replace("<", "less than").replace(">", "greater than")
        date_time = i.created_at.astimezone(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%Y %I:%M %p")
        date_time_hyperlink = INCIDENT_URL + i.id

        if incident not in rows:
            rows[incident] = {"date_time": [], "count": 0}

        rows[incident]["date_time"].append(
            f'<a href = "{date_time_hyperlink}" target="_blank">{date_time}</a>'
        )
        rows[incident]["count"] += 1
        incident_counter[incident] += 1

    sorted_incidents = incident_counter.most_common(top_n)

    incident_rows = [create_html_table_row("th", [
        "S.No.", "Incident", "Count", "Description", "Type of alert"
    ])]
    s_no = 0

    for incident, count in sorted_incidents:
        s_no += 1
        row = create_html_table_row("td", [
            s_no,
            incident,
            rows[incident]["count"],
            "",  
            ""  
        ])
        incident_rows.append(row)

    return "<table style='width: 100%; border-collapse: collapse;'>{}</table><br/>".format("".join(incident_rows))

