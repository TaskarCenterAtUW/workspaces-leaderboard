from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table

from models.metadata import metadata

changesets = Table(
    "changesets",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id")),
    Column("closed_at", DateTime),
    Column("num_changes", Integer),
)
