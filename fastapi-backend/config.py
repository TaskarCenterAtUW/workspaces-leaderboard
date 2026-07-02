from datetime import date, datetime, time, timezone
from decimal import Decimal
from email.utils import format_datetime
import html
import os
from pathlib import Path

from fastapi import Request
from dotenv import load_dotenv
from sqlalchemy import create_engine, func, select
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

load_dotenv(Path(__file__).resolve().parent / ".env")

db_host = os.environ.get("WS_OSM_DB_HOST")
db_name = os.environ.get("WS_OSM_DB_NAME")
db_password = os.environ.get("WS_OSM_DB_PASS")
db_user = os.environ.get("WS_OSM_DB_USER")

database_url = URL.create(
    "postgresql+psycopg2",
    username=db_user,
    password=db_password,
    host=db_host,
    database=db_name,
)
engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)


def get_db_session(request: Request):
    db_session = getattr(request.state, "db_session", None)
    if db_session is None:
        db_session = SessionLocal()
        request.state.db_session = db_session
    return db_session


def get_workspace_session(request: Request, workspace_id):
    db_session = get_db_session(request)
    schema_id = "workspace-" + html.escape(workspace_id)
    schema_path = f'{quote_identifier(schema_id)}, public'
    db_session.execute(
        select(func.set_config("search_path", schema_path, True)),
    )
    return db_session


def quote_identifier(identifier):
    return '"' + identifier.replace('"', '""') + '"'


def time_to_interval(selected_time):
    interval = "100 years"
    match selected_time:
        case "week":
            interval = "1 week"
        case "month":
            interval = "1 month"
        case "day":
            interval = "1 day"
    return interval


def serialize_json_value(value):
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return format_datetime(value.astimezone(timezone.utc), usegmt=True)
    if isinstance(value, date):
        value = datetime.combine(value, time(), tzinfo=timezone.utc)
        return format_datetime(value, usegmt=True)
    if isinstance(value, Decimal):
        return str(value)
    return value
