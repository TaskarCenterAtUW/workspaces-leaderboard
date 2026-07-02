from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import HTMLResponse

from health.routes import router as health_router
from leaderboard.routes import router as leaderboard_router
from profile.routes import router as profile_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leaderboard_router, prefix="/api/leaderboard")
app.include_router(profile_router, prefix="/api/leaderboard/profile")
app.include_router(health_router, prefix="/api")

FLASK_ERROR_PAGES = {
    404: (
        "404 Not Found",
        "Not Found",
        "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
    ),
    405: (
        "405 Method Not Allowed",
        "Method Not Allowed",
        "The method is not allowed for the requested URL.",
    ),
    500: (
        "500 Internal Server Error",
        "Internal Server Error",
        "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.",
    ),
}


def flask_error_response(status_code):
    title, heading, message = FLASK_ERROR_PAGES[status_code]
    return HTMLResponse(
        "<!doctype html>\n"
        "<html lang=en>\n"
        f"<title>{title}</title>\n"
        f"<h1>{heading}</h1>\n"
        f"<p>{message}</p>\n",
        status_code=status_code,
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code in FLASK_ERROR_PAGES:
        return flask_error_response(exc.status_code)
    return flask_error_response(500)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return flask_error_response(500)


@app.middleware("http")
async def close_db_session_after_request(request: Request, call_next):
    try:
        return await call_next(request)
    finally:
        db_session = getattr(request.state, "db_session", None)
        if db_session is not None:
            db_session.close()
            request.state.db_session = None
