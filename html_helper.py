def create_html_table_row(row_type, element_list):
    """Creates a table row with specified HTML element type."""
    row = "<tr>"
    for elem in element_list:
        row += f"<{row_type}>{str(elem)}</{row_type}>"
    return row + "</tr>"

def grafana_alerts_trend_section():
    """
    Returns an HTML section with an embedded Grafana alert trend image.
    """
    title_row = create_html_table_row("th", ["📊 Search Alerts Trend (Last 7 Days)"])
    image_html = (
        '<img src="https://eagleeye.swiggyops.de/d/U8gLl2p4z/search-flash-view?orgId=1&viewPanel=516&from=now-7d&to=now'
        '?panelId=516&orgId=1&from=now-7d&to=now&theme=light" '
        'style="width:700px; border:1px solid #ccc; padding:8px; border-radius:6px;" />'
    )
    image_row = create_html_table_row("td", [image_html])
    return f"<table>{title_row}{image_row}</table><br/>"

def create_html_table(headers, data):
    """Creates an HTML table with headers and data rows."""
    table = "<table border='1' style='border-collapse: collapse; width: 100%;'>"
    table += create_html_table_row("th", headers)  
    for row in data:
        table += create_html_table_row("td", row)  
    return table + "</table>"

def add_title(title, level=2, section_id=None):
    """Adds a title with an optional anchor ID for linking within the page."""
    color = "rgb(47, 54, 69)" if level != 2 else "rgb(54, 94, 50)"
    anchor = f"<a name='{section_id}'></a>" if section_id else ""
    return f"{anchor}<h{level} style='color: {color};'>{title}</h{level}>"

def add_link(url, text):
    """Adds a hyperlink."""
    return f"<a href='{url}'>{text}</a>"

def add_internal_link(section_id, text):
    """Adds an internal hyperlink to a section on the same page."""
    return f"<a href='#{section_id}'>{text}</a>"

def add_text_in_new_line(text):
    """Adds a paragraph."""
    return f"<p>{text}</p>"

def add_center_aligned_text(text):
    """Adds a center-aligned paragraph."""
    return f"<p style='text-align: center;'>{text}</p>"

def add_image(filename):
    """Embeds an image in Confluence format."""
    return f"<ac:image ac:width='100%' ><ri:attachment ri:filename='{filename}' /></ac:image>"

def horizontally_align(charts):
    """Aligns multiple charts horizontally."""
    if not charts:
        return ""
    section = "<ac:layout><ac:layout-section ac:type='two_equal'>"
    for chart in charts:
        section += f"<ac:layout-cell>{chart}</ac:layout-cell>"
    section += "</ac:layout-section></ac:layout>"
    return section

def add_oncall_tasks_section():
    """Adds the On-call Tasks section with a table."""
    section = add_title("On-call Tasks", 2, "on_call_tasks")

    # Table headers
    headers = ["Action Item", "Status", "Description", "Execution Role", "Theme"]
    
    # Empty rows for now
    data = [
        ["", "", "", "", ""],
        ["", "", "", "", ""]
    ]
    
    section += create_html_table(headers, data)
    return section

def add_search_anecdotes():

    section = add_title("Search Anecdotes", 2, "search_anecdotes")

    headers = ["BL", "Anecdote", "Status", "Description"]
    
    # Empty rows for now
    data = [
        ["", "", "", ""],
        ["", "", "", ""]
    ]
    
    section += create_html_table(headers, data)
    return section

def add_oncall_efforts_section():
    """Adds the On-call Efforts section with two tables."""
    section = add_title("On-call Efforts", 2, "on_call_efforts")

    # First table (3x5)
    headers1 = [
        "Oncall", 
        "Time spent on Anecdotes/on-call issues", 
        "TTime spent on CI/ tech execution task", 
        "Time spent on PDs", 
        "Time spent on oncall tasks",
        "Others"
    ]
    data1 = [
        ["Primary", "", "", "", "", ""],
        ["Secondary", "", "", "", "", ""]
    ]
    section += create_html_table(headers1, data1)

    # Second table (3x2)
    headers2 = ["Other Work Items", "Comments"]
    data2 = [
        ["Primary", ""],
        ["Secondary", ""]
    ]
    section += create_html_table(headers2, data2)

    return section

def create_callouts_table():
    """Creates a table for the Callouts section with 6 columns."""
    headers = [
        "<b>Issue Type [TRM / Page0 / Product Support]</b>",
        "<b>Priority</b>",
        "<b>Callout</b>",
        "<b>Impact</b>",
        "<b>Status</b>",
        "<b>Resolution and RCA</b>"
    ]

    data = [
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""]
    ]

    return add_title("Callouts", 2) + create_html_table(headers, data)

def create_high_throughput_api_table():
    """Creates a table for High Throughput API Availability."""
    headers = ["", "Availability", "Avail past week", "Description"]
    data = [
        ["/api/v3/search", "", "", ""],
        ["/api/search/suggest/v1", "", "", ""],
        ["/api/v1/search/intent", "", "", ""],
        ["scout (GetSearchResults)", "", "", ""],
        ["scout (Search)", "", "", ""],
        ["conan (Discover)", "", "", ""]
    ]
    return add_title("High Throughput API Availability", 2) + create_html_table(headers, data)

def create_expandable_sections1():
    """Creates expandable sections for Current Week Infra, Previous Week Infra, and RoCK Cost."""
    return """
    <ac:expand>
        <ac:summary>Current Week Infra</ac:summary>
        <p>Details of the current week's infrastructure costs...</p>
    </ac:expand>
    <ac:expand>
        <ac:summary>Previous Week Infra</ac:summary>
        <p>Details of the previous week's infrastructure costs...</p>
    </ac:expand>
    <ac:expand>
        <ac:summary>RoCK Cost</ac:summary>
        <p>Breakdown of RoCK-related costs...</p>
    </ac:expand>
    """

def generate_toc():
    """Generates a Table of Contents with links to sections."""
    sections = [
        ("this_week_alerts", "This Week Alerts"),
        ("high_throughput_api", "High Throughput API Availability"),
        ("callouts", "Callouts"),
        ("on_call_efforts", "On-call Efforts"),
        ("on_call_tasks", "On-call Tasks"),
        ("high_urgency_alerts", "High Urgency Alerts"),
        ("low_urgency_alerts", "Low Urgency / Warning Alerts (WIP)"),
        ("search_error_metrics", "Search Error Metrics Attribution"),
        ("actionable_items", "Actionable Items of the TRM"),
    ]
    toc = "<h2>Table of Contents</h2><ul>"
    for section_id, title in sections:
        toc += f"<li>{add_internal_link(section_id, title)}</li>"
    toc += "</ul>"
    return toc

html_content = ""
html_content += generate_toc()  # Add Table of Contents
html_content += add_title("This Week Alerts", 2, "this_week_alerts")
html_content += add_text_in_new_line("Summary of alerts for this week...")

html_content += add_title("High Throughput API Availability", 2, "high_throughput_api")
html_content += add_text_in_new_line("API availability details...")

html_content += add_title("Callouts", 2, "callouts")
html_content += add_text_in_new_line("Key callouts...")

html_content += add_title("On-call Efforts", 2, "on_call_efforts")
html_content += add_text_in_new_line("Summary of on-call efforts...")

html_content += add_title("On-call Tasks", 2, "on_call_tasks")
html_content += add_text_in_new_line("Details of on-call tasks...")

html_content += add_title("High Urgency Alerts", 2, "high_urgency_alerts")
html_content += add_text_in_new_line("Details of high urgency alerts...")

html_content += add_title("Low Urgency / Warning Alerts (WIP)", 2, "low_urgency_alerts")
html_content += add_text_in_new_line("Details of low urgency alerts...")

html_content += add_title("Search Error Metrics Attribution", 2, "search_error_metrics")
html_content += add_text_in_new_line("Metrics for search errors...")

html_content += add_title("Actionable Items of the TRM", 2, "actionable_items")
html_content += add_text_in_new_line("Key actionable items...")

print(html_content)  # This is the final HTML that can be sent to Confluence