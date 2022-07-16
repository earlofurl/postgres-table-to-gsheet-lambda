import os
import boto3
import botocore
import pygsheets
import psycopg2 as pg
import pandas as pd
import logging
import json
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# instantiate environment variables
s3_bucket = os.environ['S3_BUCKET_NAME']
g_service_acc_key = os.environ['S3_CONFIG_FILE_KEY']
db_hostname = os.environ['DB_HOSTNAME']
db_name = os.environ['DB_NAME']
db_username = os.environ['DB_USERNAME']
db_password = os.environ['DB_PASSWORD']
db_port = os.environ['DB_PORT']
db_table = os.environ['DB_TABLE_NAME']
gsheet_title = os.environ['GSHEET_TITLE']


def lambda_handler(event, context):
    logger.info('got event{}'.format(event))
    logger.error('something went wrong')

    # get service account key .json file from S3 and give local path
    s3 = boto3.client('s3')
    LOCAL_FILENAME = '/tmp/{}'.format(os.path.basename(g_service_acc_key))

    try:
        s3.download_file(Bucket=s3_bucket, Key=g_service_acc_key,
                         Filename=LOCAL_FILENAME)
        with open(LOCAL_FILENAME, 'r') as handle:
            parsed = json.load(handle)
            print(json.dumps(parsed, indent=4, sort_keys=True))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    # connect to postgres db
    conn = pg.connect(host=db_hostname,
                      dbname=db_name,
                      user=db_username,
                      password=db_password,
                      port=db_port)
    # read entire sheet into a pandas df
    df = pd.read_sql_query(f'select * from {db_table}', con=conn)

    # authorize pygsheets, open worksheet, and copy info from df to sheet
    gc = pygsheets.authorize(service_file=LOCAL_FILENAME)
    wks = gc.open(gsheet_title).sheet1
    wks.set_dataframe(df, (1, 1))
