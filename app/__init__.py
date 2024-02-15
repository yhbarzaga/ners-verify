from typing import Type

from fastapi import Depends

from app.db import get_session
from app.repositories.base import BaseRepository


def get_repository(
    repo_type: Type[BaseRepository],
):
    """Get initialized repository by type"""

    def _get_repo(
        session=Depends(get_session),
    ) -> BaseRepository:
        return repo_type(session)

    return _get_repo
