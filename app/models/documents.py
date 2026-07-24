from datetime import date
from pathlib import Path

from pydantic import BaseModel

class DocumentMetadata(BaseModel):
    document_id: str
    title: str
    department: str
    category: str
    version: str
    owner:str
    last_updated: date
    tags: list[str]

class Document(BaseModel):
    metadata: DocumentMetadata
    content: str
    source: Path

