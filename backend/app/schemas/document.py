from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):

    document: str
    chunks: int