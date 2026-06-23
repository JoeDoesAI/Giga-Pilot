import io
from typing import List

from docling.datamodel.base_models import DocumentStream
from sqlalchemy import select
from db.postgre.session import AsyncSession
from docling.document_converter import DocumentConverter
from models.postgre.file import File
from core.config import Settings
from supabase import AsyncClient
from docling.chunking import HybridChunker


class FileParser:
    def __init__(self,supabase_client:AsyncClient, db:AsyncSession):
        self.supabase = supabase_client
        self.db = db

        self.bucket = Settings.SUPABASE_BUCKET

        self.converter = DocumentConverter()
        self.chunker = HybridChunker()
        
    async def _load_docs(self) -> List[dict]:
        files = await self.supabase.strong.from_(self.bucket).list("uploads")

        if not files:
            return "No files in the supabase directory"
        
        parsed_files = []

        for file in files:
            file_name = file["name"]

            original_file_name = await self.get_original_filename(file_name)

            if file_name == ".emptyFolderPlaceholder":
                continue

            file_path = f"uploads/{file_name}"
            file_bytes = await self.supabase.storage.from_(self.bucket).download(file_path)


            buf = io.BytesIO(file_bytes)
            source = DocumentStream(name=file_name, stream=buf)

            result = self.converter.convert(source)

            
            markdown_text = result.document
        
            doc_data = {
                "filename": original_file_name,
                "file_content": markdown_text,
            }

            parsed_files.append(doc_data)

        return parsed_files 
        
    async def _chunk_files(self, parsed_files:List[dict]):
        formatted_records = []

        for file in parsed_files:
            doc_chunks = self.chunker.chunk(file.file_content)
            
            page_details = []

            for chunk in doc_chunks:
                chunk_text = self.chunker.serizlize(chunk)

                page_numbers = set()

                if hasattr(chunk, "meta") and chunk.meta.doc.items:
                    for item in chunk.meta.doc_items:
                        if hasattr(item, "prov") and item.prov:
                            for p in item.prov:
                                page_numbers.add(p.page_no)

            primary_page = min(page_numbers) if page_numbers else 1

        #at this point we have parsed per page and let's say our list

        formatted_records.append({
            "content": chunk_text,
            "meta_data": {
                "page_number": primary_page,
                "all_spanned_pages": list(page_numbers),
                "heading": chunk.meta.headings[0] if chunk.meta.heading else None
            }
        })



    async def _get_original_filename(self,file_name:str) -> str:
        get_filename = select(File.original_name).where(File.stored_name == file_name)
        result = await self.db.execute(get_filename)

        original_name = result.scalar_one_or_none()

        return original_name


"""
list per page of the document

that would include 
- original file name
- page number
- page content
- page_char_count
- page token_count




"""












