# BUILD SEARCH TRM 

## Steps to run:
1. Create a virtual environment: python3 -m venv myenv
2. Activate the virtual environment: source myenv/bin/activate
3. Install the required packages: pip3 install -r requirements.txt
4. To generate keys:
OpsGenie API: https://bundltechnologies.app.opsgenie.com/settings/api-key-management
Atlassian API Token: https://id.atlassian.com/manage-profile/security/api-tokens
4. Set the Confluence page auth token: export CONFLUENT_PAGE_AUTH_TOKEN=<atlassian_api_key>
5. Set the OpsGenie API key: export OPS_GENIE_API_KEY=<opsgenie_api_key>
6. Update emailId in config.py
7. Run the following on Snowflake: SELECT presentableEntity, COUNT(*) AS total, searchError FROM "STREAMS"."PUBLIC"."SAND_SEARCH_EVENT" WHERE dt BETWEEN 'yyyy-mm-dd' AND 'yyyy-mm-dd' GROUP BY presentableEntity, searchError;, then download the result as a CSV and save it in this folder.
8. Run python error_metrics.py <csv_file_name>
9. Run the main script: python3 main.py