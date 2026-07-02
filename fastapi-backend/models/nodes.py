from sqlalchemy import Column, ForeignKey, Integer, Table

from models.metadata import metadata

nodes = Table(
    "nodes",
    metadata,
    Column("changeset_id", ForeignKey("changesets.id")),
    Column("latitude", Integer),
    Column("longitude", Integer),
)
