import pandas as pd
from .email_client import get_unread_emails, mark_emails_as_read
from .parser import extract_date_and_table
from .loader_bq import load_to_bigquery

def main():
    mail, email_ids, emails_content = get_unread_emails()
    all_errors_df = pd.DataFrame()

    for email_id, email_content in emails_content:
        errors_df = extract_date_and_table(email_content)
        all_errors_df = pd.concat([all_errors_df, errors_df], ignore_index=True)

    if not all_errors_df.empty:
        load_to_bigquery(all_errors_df)
        mark_emails_as_read(mail, email_ids)  # Mark processed emails as read
    else:
        print("No unread emails found matching criteria.")
        mail.logout()
