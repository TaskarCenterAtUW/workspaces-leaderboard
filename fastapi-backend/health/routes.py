from fastapi import APIRouter
from sqlalchemy import text

from config import SessionLocal

router = APIRouter()


@router.get("/health")
def get_health():
    db_status = "ok"
    db_error = None

    try:
        with SessionLocal() as db_session:
            db_session.execute(text("SELECT 1"))
    except Exception as exc:
        db_status = "error"
        db_error = str(exc)

    response = {
        "status": "ok",
        "database": {
            "status": db_status,
        },
    }

    if db_error:
        response["database"]["error"] = db_error

    return response
