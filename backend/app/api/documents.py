from fastapi import APIRouter, UploadFile, File

from app.schemas.document import (
    DocumentUploadResponse,
)

from app.services.rag.service import (
    ingest_document,
)


router = APIRouter()


@router.post(
    "/documents",
    response_model=DocumentUploadResponse,
)
async def upload_document(
    document: UploadFile = File(...),
):

    content = await document.read()

    result = ingest_document(
        filename=document.filename,
        content=content,
    )

    return DocumentUploadResponse(
        **result
    )