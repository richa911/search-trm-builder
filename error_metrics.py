import pandas as pd
import sys

if len(sys.argv) < 2:
    print("Usage: python script.py <csv_filename>")
    sys.exit(1)

csv_filename = sys.argv[1]
df = pd.read_csv(csv_filename)

# Get the baseline NONE values per PRESENTABLEENTITY
none_totals = df[df["SEARCHERROR"] == "NONE"].set_index("PRESENTABLEENTITY")["TOTAL"].to_dict()

# Filter out NONE rows for calculations
errors_df = df[df["SEARCHERROR"] != "NONE"]

# Compute percentage relative to NONE total
def compute_percentage(row):
    base_total = none_totals.get(row["PRESENTABLEENTITY"], None)
    if base_total and base_total != 0:
        return (row["TOTAL"] / base_total) * 100
    else:
        return None

errors_df["PERCENT_OF_NONE"] = errors_df.apply(compute_percentage, axis=1)

# Optional: Sort and clean the output
errors_df = errors_df.sort_values(by=["PRESENTABLEENTITY", "SEARCHERROR"])

# Display result
print(errors_df[["PRESENTABLEENTITY", "SEARCHERROR", "TOTAL", "PERCENT_OF_NONE"]])

# List of desired columns and rows
error_types = [
    "DATA_PROVIDER_EXCEPTION",
    "EMPTY_SEARCH_RESULTS_EXCEPTION",
    "ITEM_ORDERABILITY_EXCEPTION",
    "RESTAURANT_ENTITY_EXCEPTION",
    "RESTAURANT_MENU_ITEMS_ENTITY_EXCEPTION",
    "RESTAURANT_ORDERABILITY_EXCEPTION"
]

entities = [
    "ITEM",
    "RESTAURANT",
    "RESTAURANT_ITEM",
    "RESTAURANT_SIMILAR_NAME",
    "RESTAURANT_WITH_ITEMS"
]

# Create pivot table with zeros where no data
pivot = errors_df.pivot_table(
    index="PRESENTABLEENTITY",
    columns="SEARCHERROR",
    values="PERCENT_OF_NONE",
    aggfunc="sum",
    fill_value=0
)

# Reindex to ensure correct order and include only required values
pivot = pivot.reindex(index=entities, columns=error_types, fill_value=0)

grand_total = pivot.sum()
pivot.loc["Grand Total"] = grand_total

pivot.reset_index(inplace=True)
pivot.rename(columns={"PRESENTABLEENTITY": " "}, inplace=True)

# Save to CSV
pivot.to_csv("search_error_metrics_summary.csv", index=False)

print("✅ Error metrics table saved to: search_error_metrics_summary.csv")
