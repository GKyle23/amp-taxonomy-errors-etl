from google.oauth2 import service_account
from google.cloud import bigquery
import imaplib
import email
import pandas as pd
import re

# Config
GMAIL_USERNAME = "your_email@gmail.com"
GMAIL_PASSWORD = "your_password"
IMAP_SERVER = "imap.gmail.com"
BIGQUERY_PROJECT_ID = "your-gcp-project-id"
BIGQUERY_DATASET_ID = "your_dataset"
BIGQUERY_TABLE_ID = "your_table"
SERVICE_ACCOUNT_FILE = "your-service-account.json"

SUBJECT_FILTER = '[Amplitude] Taxonomy Validation Errors for '  # Subject prefix filter

# Search for unread emails where the subject starts with '[Amplitude] Taxonomy Validation Errors for'
def get_unread_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    mail.select("inbox")

    # Search for unread emails where the subject starts with '[Amplitude] Taxonomy Validation Errors for'
    search_criteria = f'(UNSEEN SUBJECT "{SUBJECT_FILTER}")'
    result, data = mail.search(None, search_criteria)

    email_ids = data[0].split()
    emails_content = []

    for email_id in email_ids:
        result, msg_data = mail.fetch(email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    email_content = part.get_payload(decode=True).decode()
                    emails_content.append((email_id, email_content))
                    break
        else:
            email_content = msg.get_payload(decode=True).decode()
            emails_content.append((email_id, email_content))

    return mail, email_ids, emails_content

# ---- EXTRACT DATE AND ERROR TABLE ----
def extract_date_and_table(email_content):
    # Extract Date using Regex
    date_match = re.search(r"Date:\s*([\d-]+)", email_content)
    date_value = date_match.group(1) if date_match else "Unknown"

    # Extract Table using Pandas (assuming HTML format)
    tables = pd.read_html(email_content)
    error_table = tables[0]  # Assuming the first table contains error data
    error_table["date"] = date_value  # Add extracted date to table

    return error_table

# Load data to Big Query
def load_to_bigquery(df):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    client = bigquery.Client(credentials=credentials, project=BIGQUERY_PROJECT_ID)

    table_ref = f"{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET_ID}.{BIGQUERY_TABLE_ID}"
    job = client.load_table_from_dataframe(df, table_ref)
    job.result()  # Wait for job completion

    print("Data loaded into Big Query")

# Mark emails as read
def mark_emails_as_read(mail, email_ids):
    for email_id in email_ids:
        mail.store(email_id, "+FLAGS", "\\Seen")
    mail.logout()

# Boom
if __name__ == "__main__":
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
