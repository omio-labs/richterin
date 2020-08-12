# Great Expectations Service

### Running the service:
1.  Create a configuration file with following properties:
      1.  GCP_PROJECT_ID
      2.  BIGQUERY_TEMP_TABLE_DATASET: Dataset that will be used for creating temporary tables by Great expectations. It's nice to have autodelete lifecycle for this dataset.
      3.  GOOGLE_APPLICATION_CREDENTIALS : Path to google credentials json file

2. Create an environment variable **GE_SERVICE_SETTINGS** with value configured to the configuration file.
   e.g. export GE_SERVICE_SETTINGS=/path/to/settings.cfg

3. Run the service.py file
