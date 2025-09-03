from google.oauth2 import service_account
from google.cloud import bigquery
from .config import SERVICE_ACCOUNT_FILE, BIGQUERY_PROJECT_ID, BIGQUERY_DATASET_ID, BIGQUERY_TABLE_ID

# Load data to Big Query
def load_to_bigquery(df):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    client = bigquery.Client(credentials=credentials, project=BIGQUERY_PROJECT_ID)

    table_ref = f"{BIGQUERY_PROJECT_ID}.{BIGQUERY_DATASET_ID}.{BIGQUERY_TABLE_ID}"
    job = client.load_table_from_dataframe(df, table_ref)
    job.result()  # Wait for job completion

    print("Data loaded into Big Query")
