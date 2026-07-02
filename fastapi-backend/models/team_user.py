from sqlalchemy import Column, ForeignKey, Table

from models.metadata import metadata

team_user = Table(
    "team_user",
    metadata,
    Column("team_id", ForeignKey("teams.id")),
    Column("user_id", ForeignKey("users.id")),
)
