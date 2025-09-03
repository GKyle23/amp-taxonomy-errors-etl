from google.oauth2 import service_account  # not used here directly, but kept for parity

# Config (UNCHANGED VALUES/VARIABLE NAMES)
GMAIL_USERNAME = "your_email@gmail.com"
GMAIL_PASSWORD = "your_password"
IMAP_SERVER = "imap.gmail.com"
BIGQUERY_PROJECT_ID = "your-gcp-project-id"
BIGQUERY_DATASET_ID = "your_dataset"
BIGQUERY_TABLE_ID = "your_table"
SERVICE_ACCOUNT_FILE = "your-service-account.json"

SUBJECT_FILTER = '[Amplitude] Taxonomy Validation Errors for '  # Subject prefix filter
