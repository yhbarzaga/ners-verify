from fastapi import APIRouter, Depends, HTTPException, status

from app import get_repository
from app.exceptions import ResourceNotFound
from app.repositories import StaffRepository
from app.services.staff_service import StaffService

router = APIRouter()


@router.get("/staff/{staff_id}")
def process_document(
    staff_id: str,
    staff_repo=Depends(get_repository(StaffRepository)),
):
    """Get the total amount to be refund for the given staff"""

    try:
        return StaffService(repo=staff_repo).get_total(staff_id)
    except ResourceNotFound as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
