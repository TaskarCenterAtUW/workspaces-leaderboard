from flask import g
import psycopg2
import os

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
