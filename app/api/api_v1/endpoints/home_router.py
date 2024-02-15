from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from starlette import status

from app.db.session import SessionLocal

router = APIRouter()


@router.get("/health-check")
def health_check() -> dict:
    """
    Health check endpoint for the API.
    """
    try:
        # check connectivity to all databases
        db = SessionLocal()
        # Try to create a session to check if DB is awake
        db.execute(text("SELECT 1"))
        return {"message": "OK", "timestamp": datetime.now().isoformat()}
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(err)
        ) from err
