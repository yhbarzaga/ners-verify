from fastapi import APIRouter, Depends, HTTPException, status

from app import get_repository
from app.api import verify
from app.exceptions import ResourceNotFound
from app.repositories import DocumentRepository, StaffRepository
from app.schemas import DocumentCreateSchema
from app.services.ocr_processing import ProcessDocumentData
from app.services.ocr_processing.ocr_exceptions import OCRDocumentException
from app.services.ocr_processing.ocr_service import OCRService
from app.services.ocr_processing.providers import get_ocr_provider
from app.services.staff_service import StaffService

router = APIRouter()


@router.post(
    "/documents", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify)]
)
def process_document(
    payload: DocumentCreateSchema,
    ocr_provider=Depends(get_ocr_provider),
    document_repo=Depends(get_repository(DocumentRepository)),
    staff_repo=Depends(get_repository(StaffRepository)),
):
    """Process document through the OCR provider to storage information in the database"""

    try:
        staff = StaffService(repo=staff_repo).get_by_internal_id(payload.staff_id)

        OCRService(
            ocr_provider=ocr_provider,
            repo=document_repo,
        ).process(
            staff_id=staff.uid,
            document=ProcessDocumentData(**payload.dict(exclude={"staff_id"})),
        )

    except ResourceNotFound as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    except OCRDocumentException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail) from err
