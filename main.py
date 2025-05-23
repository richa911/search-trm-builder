import os
from decouple import config as configEnv
import config, opsgenie
from confluence import create_confluence_page, upload_image_attachment, update_confluence_page
import html_helper, analytics_helper, links, helper

def validate(configs):
    missing_fields = [field for field in ['emailID', 'teamName', 'parentPageID', 'spaceId'] if
                      not getattr(configs, field)]
    if missing_fields:
        print(', '.join(missing_fields) + " missing from config")
        return False
    return True

def generate_piechart_weeklychart_section(team_alerts):
    pie_charts = []
    weekly_graphs = []

    team_name = config.teamName 

    data = {}
    total_alerts = 0

    # Get Critical Alerts (P1)
    critical_alerts = team_alerts[team_name + "-critical"]
    total_alerts += len(critical_alerts)
    data['Critical'] = len(critical_alerts)

    # Get Warning Alerts (P2 + P3)
    warning_alerts = team_alerts[team_name + "-warning"]
    total_alerts += len(warning_alerts)
    data['Warning'] = len(warning_alerts)

    # Create Pie Chart
    file_name = analytics_helper.create_pie_chart_image(
        data, team_name + " Alerts Breakdown", "temp/" + team_name + "-alert-piechart.png"
    )
    image = html_helper.add_image(upload_image_attachment(file_name, page_id, "Total Alerts: " + str(total_alerts)))
    image += html_helper.add_center_aligned_text("Total Alerts: " + str(total_alerts))
    pie_charts.append(image)

    # Prepare data for Weekly Bar Graph
    graph_data = {}
    for criticalAlert in critical_alerts:
        date = criticalAlert.created_at.strftime("%d-%m-%Y")
        if date not in graph_data:
            graph_data[date] = {'Critical': 0, 'Warning': 0}
        graph_data[date]['Critical'] += 1

    for warningAlert in warning_alerts:
        date = warningAlert.created_at.strftime("%d-%m-%Y")
        if date not in graph_data:
            graph_data[date] = {'Critical': 0, 'Warning': 0}
        graph_data[date]['Warning'] += 1

    # Create Weekly Alerts Bar Graph
    file_name = analytics_helper.plot_alerts_per_day(
        graph_data, team_name + " Alerts Per Day", "temp/" + team_name + "-alert-graph.png"
    )
    weekly_graphs.append(html_helper.add_image(upload_image_attachment(file_name, page_id)))

    return pie_charts, weekly_graphs

if __name__ == "__main__":
    if not validate(config):
        print("Config is not valid")
        exit()

    sections = html_helper.add_title("This is an empty page", 2)
    # Create Confluence Page
    page_id = create_confluence_page(parent_page_id=config.parentPageID,
                                     email_id=config.emailID,
                                     auth_token=(configEnv('CONFLUENT_PAGE_AUTH_TOKEN')),
                                     html_content=sections,
                                     space_id=config.spaceId)
    
    sections = html_helper.generate_toc()  # Generates Table of Contents

    os.makedirs("temp", exist_ok=True)  # Create temp directory if not exists

    teamName = config.teamName  
    # Get current week alerts
    teamAlerts = {
        teamName + "-critical": opsgenie.list_alerts(teamName, priority='P1'),
        teamName + "-warning": opsgenie.list_alerts(teamName, priority='P2') +
                            opsgenie.list_alerts(teamName, priority='P3')
    }
    # Get last week alerts
    teamAlerts_lw = {
        teamName + "-critical": opsgenie.list_alerts_lw(teamName, priority='P1'),
        teamName + "-warning": opsgenie.list_alerts_lw(teamName, priority='P2') +
                            opsgenie.list_alerts_lw(teamName, priority='P3')
    }

    # Generate Pie Chart & Weekly Bar Graphs
    pieCharts, weeklyGraphs = generate_piechart_weeklychart_section(teamAlerts)

    # Add Pie Chart to Confluence Page
    sections += html_helper.horizontally_align(pieCharts)

    # Add Weekly Bar Graphs
    for weeklyGraph in weeklyGraphs:
        sections += weeklyGraph

    table_data = [
        [f"Total PD: {len(teamAlerts_lw[teamName + '-critical']) + len(teamAlerts_lw[teamName + '-warning'])}", f"Total PD: {len(teamAlerts[teamName + '-critical']) + len(teamAlerts[teamName + '-warning'])}", ""],
        [f"Critical Alerts: {len(teamAlerts_lw[teamName + '-critical'])}", f"Critical Alerts: {len(teamAlerts[teamName + '-critical'])}", ""],
        [f"Warnings: {len(teamAlerts_lw[teamName + '-warning'])}", f"Warnings: {len(teamAlerts[teamName + '-warning'])}", ""],
        ["External:\n Critical:\n Warnings:", "External:\n Critical:\n Warnings:", ""],
        ["Internal:\n Critical:\n Warnings:", "Internal:\n Critical:\n Warnings:", ""]
    ]
    # Table Headers
    table_headers = ["Last TRM PD Count", "This TRM PD Count", "Comments"]

    # Convert the table to HTML format using the helper function
    sections += html_helper.create_html_table(table_headers, table_data)

    # Infra Cost Table 
    infra_cost_table_headers = ["", "Rock", "Non-Rock", ""]
    infra_cost_table_data = [
        ["This Week", "", "", ""],
        ["Last Week", "", "", ""],
        ["% Delta from last week", "", "", ""],
        ["Details", "", "", ""]
    ]
    sections += html_helper.add_title("Infra Cost Breakdown", 2)
    sections += html_helper.create_html_table(infra_cost_table_headers, infra_cost_table_data)


    # Adding Sections
    sections += html_helper.create_expandable_sections1()

    sections += html_helper.create_high_throughput_api_table()

    sections += html_helper.create_callouts_table()

    sections += html_helper.add_oncall_efforts_section()

    sections += html_helper.add_oncall_tasks_section()

    sections += html_helper.add_search_anecdotes()

    # Get P1 alerts for the team and convert them to a table
    sections += opsgenie.convert_resp_to_table(
    opsgenie.list_alerts(team=teamName, priority='P1'),
    'High Urgency Alerts',
    opsgenie.list_alerts_lw(team=teamName, priority='P1'))


    sections += html_helper.add_title("Low Urgency / Warning Alerts (WIP)", 2)

    # Get P3 alerts for the team and convert them to a table
    alerts = opsgenie.list_alerts(team=teamName, priority='P3')
    sections += html_helper.add_title(teamName, 4)
    sections += opsgenie.convert_resp_to_analytics_table(alerts, config.numberOfWarningAlerts)

    # Add section for Canary rejection, hot fix, build times, etc.
    sections += html_helper.add_title("Canary Rejection, Hot Fix, Build Times, etc.", 2, "canary_rejection")

    # Placeholder for manually adding the link
    sections += html_helper.add_center_aligned_text("🔗 Add the link here ")
    sections += "<br/><br/>"  

    # Add section for Search Error Metrics Attribution
    sections += html_helper.add_title("Search Error Metrics Attribution", 2, "search_error_metrics")

    # Subsections for This Week’s and Last Week’s Error Attribution
    sections += html_helper.add_title("This Week’s Error Attribution", 3, "this_week_error_attribution")
    sections += helper.build_search_error_summary_table_from_csv("search_error_metrics_summary.csv")

    sections += html_helper.add_title("Last Week’s Error Attribution", 3, "last_week_error_attribution")
    sections += "<br/><br/>"

    # Add section for Actionable Items of the TRM
    sections += html_helper.add_title("Actionable Items of the TRM", 2, "actionable_items")

    # Create table structure for Actionable Items of the TRM
    actionable_items_table = html_helper.create_html_table(
        headers=["Task Details", "Relevant Links", "Jira Ticket", "Stack Rank", "Assignee", "Comments"],
        data=[["", "", "", "", "", ""],  
          ["", "", "", "", "", ""]]  
    )

    sections += actionable_items_table
    sections += "<br/><br/>"

    links.open_grafana_dashboards()
    links.open_cost_explorer_chart()

    # Updating Confluence Page
    update_confluence_page(page_id=page_id,
                           email_id=config.emailID,
                           auth_token=(configEnv('CONFLUENT_PAGE_AUTH_TOKEN')),
                           html_content=sections.replace('&', '&amp;'))

    os.system("rm -r temp")  # Cleanup temp directory
