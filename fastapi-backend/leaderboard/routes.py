from fastapi import APIRouter, Request
from sqlalchemy import bindparam, cast, func, select
from sqlalchemy.dialects.postgresql import INTERVAL

from config import serialize_json_value, get_workspace_session, time_to_interval
from models import changesets, team_user, teams, users

router = APIRouter()


def fetch_leaderboard(request: Request, filterTeam=None, filterTime=None, filterWorkspace=None):
    db_session = get_workspace_session(request, filterWorkspace)

    match filterTeam:
        case "team":
            score = func.sum(func.coalesce(changesets.c.num_changes, 0)).label("score")
            query = (
                select(
                    teams.c.id.label("id"),
                    teams.c.name,
                    score,
                )
                .select_from(
                    teams.join(team_user, teams.c.id == team_user.c.team_id)
                    .join(users, team_user.c.user_id == users.c.id)
                    .outerjoin(
                        changesets,
                        (changesets.c.user_id == users.c.id)
                        & (
                            changesets.c.closed_at
                            >= func.now() - cast(bindparam("interval"), INTERVAL)
                        ),
                    )
                )
                .where(teams.c.workspace_id == bindparam("workspace_id"))
                .group_by(teams.c.name, teams.c.id)
                .order_by(score.desc())
            )
            params = {
                "interval": time_to_interval(filterTime),
                "workspace_id": filterWorkspace,
            }
        case _:
            score = func.sum(changesets.c.num_changes).label("score")
            query = (
                select(
                    users.c.id.label("id"),
                    users.c.display_name.label("name"),
                    score,
                )
                .select_from(changesets.join(users, changesets.c.user_id == users.c.id))
                .where(
                    changesets.c.closed_at
                    >= func.now() - cast(bindparam("interval"), INTERVAL)
                )
                .group_by(users.c.display_name, users.c.id)
                .order_by(score.desc())
            )
            params = {"interval": time_to_interval(filterTime)}

    rows = db_session.execute(query, params).all()
    return [
        {
            "id": serialize_json_value(row[0]),
            "name": serialize_json_value(row[1]),
            "score": serialize_json_value(row[2]),
        }
        for row in rows
    ]


@router.get("/")
def get_leaderboard(
    request: Request,
    filterTeam: str | None = None,
    filterTime: str | None = None,
    filterWorkspace: str | None = None,
):
    return fetch_leaderboard(request, filterTeam, filterTime, filterWorkspace)


@router.get("", include_in_schema=False)
def get_leaderboard_without_slash(
    request: Request,
    filterTeam: str | None = None,
    filterTime: str | None = None,
    filterWorkspace: str | None = None,
):
    return fetch_leaderboard(request, filterTeam, filterTime, filterWorkspace)
