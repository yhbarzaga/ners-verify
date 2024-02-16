from fastapi import APIRouter, Depends, HTTPException, status

from app import get_repository
from app.api import verify
from app.exceptions import ResourceNotFound
from app.repositories import StaffRepository
from app.services.staff_service import StaffService

router = APIRouter()


@router.get("/staff/{staff_id}/refund", dependencies=[Depends(verify)])
def get_total_refund(
    staff_id: str,
    staff_repo=Depends(get_repository(StaffRepository)),
):
    """Get the total amount to be refund for the given staff"""

    try:
        return StaffService(repo=staff_repo).get_total(staff_id)
    except ResourceNotFound as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(err)
        ) from err
