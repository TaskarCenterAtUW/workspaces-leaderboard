from fastapi import APIRouter, Request
from sqlalchemy import bindparam, cast, literal, select
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import INTERVAL

from config import serialize_json_value, get_workspace_session, time_to_interval
from models import changesets, nodes, team_user, teams, users

router = APIRouter()


def fetch_profile_map(request: Request, filterId=None, filterTeam=None, filterTime=None, filterWorkspace=None):
    db_session = get_workspace_session(request, filterWorkspace)

    query = (
        select(changesets.c.id, nodes.c.latitude, nodes.c.longitude)
        .where(
            changesets.c.closed_at
            >= func.now() - cast(bindparam("interval"), INTERVAL)
        )
    )

    match filterTeam:
        case "team":
            query = query.select_from(
                changesets.join(nodes, changesets.c.id == nodes.c.changeset_id)
            )
            team_users = select(team_user.c.user_id).where(
                team_user.c.team_id == bindparam("filter_id")
            )
            query = query.where(changesets.c.user_id.in_(team_users))
        case _:
            query = query.select_from(
                changesets.join(nodes, changesets.c.id == nodes.c.changeset_id)
            )
            query = query.where(changesets.c.user_id == bindparam("filter_id"))

    rows = db_session.execute(
        query,
        {
            "interval": time_to_interval(filterTime),
            "filter_id": filterId,
        },
    ).all()
    return [
        {
            "id": serialize_json_value(row[0]),
            "latitude": serialize_json_value(row[1]),
            "longitude": serialize_json_value(row[2]),
        }
        for row in rows
    ]


def fetch_profile_stats(request: Request, filterId=None, filterTeam=None, filterWorkspace=None):
    db_session = get_workspace_session(request, filterWorkspace)

    match filterTeam:
        case "team":
            query = select(
                teams.c.id,
                teams.c.name,
                literal("").label("created"),
            ).where(teams.c.id == bindparam("filter_id"))
        case _:
            query = select(
                users.c.id,
                users.c.display_name.label("name"),
                users.c.creation_time.label("created"),
            ).where(users.c.id == bindparam("filter_id"))

    row = db_session.execute(query, {"filter_id": filterId}).first()
    return {
        "id": serialize_json_value(row[0]),
        "name": serialize_json_value(row[1]),
        "created": serialize_json_value(row[2]),
    }


@router.get("/map/")
def get_profile_map(
    request: Request,
    filterId: str | None = None,
    filterTeam: str | None = None,
    filterTime: str | None = None,
    filterWorkspace: str | None = None,
):
    return fetch_profile_map(request, filterId, filterTeam, filterTime, filterWorkspace)


@router.get("/map", include_in_schema=False)
def get_profile_map_without_slash(
    request: Request,
    filterId: str | None = None,
    filterTeam: str | None = None,
    filterTime: str | None = None,
    filterWorkspace: str | None = None,
):
    return fetch_profile_map(request, filterId, filterTeam, filterTime, filterWorkspace)


@router.get("/stats/")
def get_profile_stats(
    request: Request,
    filterId: str | None = None,
    filterTeam: str | None = None,
    filterWorkspace: str | None = None,
):
    return fetch_profile_stats(request, filterId, filterTeam, filterWorkspace)


@router.get("/stats", include_in_schema=False)
def get_profile_stats_without_slash(
    request: Request,
    filterId: str | None = None,
    filterTeam: str | None = None,
    filterWorkspace: str | None = None,
):
    return fetch_profile_stats(request, filterId, filterTeam, filterWorkspace)
