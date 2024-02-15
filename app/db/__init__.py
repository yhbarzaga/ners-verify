from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_session() -> Session:
    """Get services db session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
