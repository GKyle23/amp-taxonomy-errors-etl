import pandas as pd
import re

# ---- EXTRACT DATE AND ERROR TABLE ----
def extract_date_and_table(email_content):
    # Extract Date using Regex
    date_match = re.search(r"Date:\s*([\d-]+)", email_content)
    date_value = date_match.group(1) if date_match else "Unknown"

    # Extract Table using Pandas
    tables = pd.read_html(email_content)
    error_table = tables[0]  # Assuming the first table contains error data
    error_table["date"] = date_value  # Add extracted date to table

    return error_table

