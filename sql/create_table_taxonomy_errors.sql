CREATE SCHEMA IF NOT EXISTS `${GCP_PROJECT}.${BQ_DATASET}`;

CREATE TABLE IF NOT EXISTS `${GCP_PROJECT}.${BQ_DATASET}.${BQ_TABLE}` (
  event_name STRING,
  property_name STRING,
  violation_type STRING,
  expected STRING,
  actual STRING,
  source_email_id STRING,
  occurred_at TIMESTAMP,
  received_at TIMESTAMP,
  project_tag STRING,
  load_at TIMESTAMP
)
PARTITION BY DATE(occurred_at)
CLUSTER BY event_name, violation_type;
