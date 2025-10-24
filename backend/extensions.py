from flask import g
import html
import os
import psycopg2

# Access the environment variables
db_host = os.environ.get("WS_OSM_DB_HOST")
db_name = os.environ.get("WS_OSM_DB_NAME")
db_password = os.environ.get("WS_OSM_DB_PASS")
db_user = os.environ.get("WS_OSM_DB_USER")

def get_db_connection():
    if 'db_conn' not in g:
        g.db_conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
    return g.db_conn

def close_db_connection(exception=None):
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()

def get_workspace_cursor(workspaceId):
    conn = get_db_connection()
    cursor = conn.cursor()

    schema_query = "SET search_path TO %s, public;"
    schemaId = "workspace-" + html.escape(workspaceId)
    cursor.execute(schema_query, (schemaId,))
    return cursor

def time_to_interval(time):
    interval = '100 years'
    match time:
        case 'week':
            interval = '1 week'
        case 'month':
            interval = '1 month'
        case 'day':
            interval = '1 day'
    return interval