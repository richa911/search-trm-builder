import pandas as pd
import html_helper

def build_search_error_summary_table_from_csv(csv_path="search_error_metrics_summary.csv"):
    # Read the CSV
    df = pd.read_csv(csv_path)

    for col in df.columns[1:]:  
        df[col] = df[col].apply(lambda x: f"{float(x):.8f}%" if pd.notnull(x) else "0.00%")

    # Extract headers and data
    headers = list(df.columns)
    data = df.values.tolist()

    # Return HTML table
    return html_helper.create_html_table(headers=headers, data=data)
