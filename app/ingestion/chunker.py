from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter
)


from app.models.documents import Document
from app.models.chunks import Chunk, ChunkMetadata


class DocumentChunker:

    def __init__(self, chunk_size:int = 500, chunk_overlap:int = 100):
        self.header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#","h1"), # Split on # and tag them as h1
                ("##","h2"),
                ("###","h3")
            ],
            strip_headers=False #header lines will be included in the chunks.
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap
        )
    
    def chunk(self, document:Document)->list[Chunk]:
        """Convert docs into chunks"""

        header_sections = self.header_splitter.split_text(document.content)
        #print(f"{document.metadata.title}: {len(header_sections)} header sections")

        chunks:list[Chunk] = []
        
        chunk_index = 0

        for section in header_sections:
            #print(section.metadata)
            split_text = self.text_splitter.split_text(
                section.page_content                
            )

            heading_path = []

            if 'h1' in section.metadata:
                heading_path.append(section.metadata["h1"])
            if "h2" in section.metadata:
                heading_path.append(section.metadata["h2"])
            if "h3" in section.metadata:
                heading_path.append(section.metadata["h3"])
            
            heading_level = len(heading_path)


            for text in split_text:
                metadata = ChunkMetadata(
                    chunk_id=f"{document.metadata.document_id}_{chunk_index}",
                    document_id=document.metadata.document_id,
                    title=document.metadata.title,
                    department=document.metadata.department,
                    category=document.metadata.category,
                    version=document.metadata.version,
                    section=section.metadata.get("h1", ""),
                    subsection=section.metadata.get("h2"),
                    heading_path=heading_path,
                    heading_level=heading_level,
                    chunk_index=chunk_index,
                    tags=document.metadata.tags,
                )

                chunks.append(
                    Chunk(
                        metadata=metadata,
                        content=text,
                        source=document.source,
                    )
                )

                chunk_index +=1
        return chunks

        

