from sqlalchemy import Column, Integer, String, Table

from models.metadata import metadata

teams = Table(
    "teams",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("workspace_id", String),
)
