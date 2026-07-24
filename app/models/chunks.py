from pathlib import Path
from pydantic import BaseModel

class ChunkMetadata(BaseModel):
    chunk_id:str
    document_id:str

    title:str
    department:str
    category:str
    version:str

    section:str
    subsection: str|None = None
    heading_path: list[str]
    heading_level: int
    
    chunk_index: int

    tags: list[str]


class Chunk(BaseModel):
    metadata: ChunkMetadata
    content: str
    source: Path