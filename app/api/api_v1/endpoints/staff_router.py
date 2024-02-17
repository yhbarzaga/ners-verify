from fastapi import APIRouter, Depends, HTTPException, status

from app import get_repository
from app.api import verify
from app.domain import StaffCreateDomain
from app.exceptions import ResourceNotFound, CreationError
from app.repositories import StaffRepository
from app.schemas import StaffCreateSchema, StaffResponseSchema
from app.services.staff_service import StaffService

router = APIRouter()


@router.get("/staff/{internal_id}/refund", dependencies=[Depends(verify)])
def get_total_refund(
    internal_id: str,
    staff_repo=Depends(get_repository(StaffRepository)),
):
    """Get the total amount to be refund for the given staff"""

    try:
        return StaffService(repo=staff_repo).get_total(internal_id)
    except ResourceNotFound as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(err)
        ) from err


@router.post(
    "/staff",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify)],
    response_model=StaffResponseSchema,
)
def create_staff(
    payload: StaffCreateSchema,
    staff_repo=Depends(get_repository(StaffRepository)),
):
    """
    Create a new member of the staff
    Use uid value in response whenever required staff_id
    """

    try:
        return StaffService(repo=staff_repo).create(StaffCreateDomain(**payload.dict()))
    except CreationError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(err)
        ) from err
