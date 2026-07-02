from sqlalchemy import Column, DateTime, Integer, String, Table

from models.metadata import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("display_name", String),
    Column("creation_time", DateTime),
)
