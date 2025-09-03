[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

Extract–Transform–Load (ETL) pipeline that ingests **Amplitude Taxonomy Validation Error** notification emails from an IMAP inbox, parses the error tables, and loads them into **BigQuery** for monitoring and reporting.

---

## ✨ Why this project?
Amplitude surfaces **validation errors** (unplanned events, invalid properties, etc.) in its UI and email notifications. Those errors are valuable for:
- Monitoring data quality trends over time  
- Automating alerts for broken instrumentation  
- Giving product & data teams visibility without manually checking Amplitude’s UI  

This ETL automates that process:  
**Fetch** → Amplitude error emails via IMAP  
**Parse** → extract error tables & timestamps  
**Load** → append to a BigQuery table for analysis & dashboards  

---

# amp-taxonomy-errors-etl

Run locally:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
amp-tax-etl
