import os
from datetime import timedelta
BASE_DIR=os.path.abspath(os.path.dirname(__file__))

# Vercel's serverless functions run on a read-only filesystem — only /tmp is
# writable, and it's wiped between invocations. Locally (BASE_DIR) stays
# writable, so we only switch to /tmp when actually running on Vercel.
IS_VERCEL = os.environ.get("VERCEL") == "1"
DATA_DIR = "/tmp" if IS_VERCEL else BASE_DIR

class Config:
    SECRET_KEY=os.environ.get("SECRET_KEY","dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(DATA_DIR, "resume.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    UPLOAD_FOLDER=os.path.join(DATA_DIR,"uploads")
    MAX_CONTENT_LENGTH=8*1024*1024

    # Keep authentication alive until the user explicitly logs out.
    # Flask-Login's remember cookie restores the session after refresh/restart.
    PERMANENT_SESSION_LIFETIME=timedelta(days=3650)
    SESSION_COOKIE_HTTPONLY=True
    SESSION_COOKIE_SAMESITE="Lax"
    REMEMBER_COOKIE_DURATION=timedelta(days=3650)
    REMEMBER_COOKIE_HTTPONLY=True
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST=True
    SESSION_COOKIE_SECURE=IS_VERCEL
    REMEMBER_COOKIE_SECURE=IS_VERCEL
