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
    def __init__(self, supabase_client: AsyncClient, db: AsyncSession):
        self.supabase = supabase_client
        self.db = db

        self.bucket = Settings.SUPABASE_BUCKET

        self.converter = DocumentConverter()
        self.chunker = HybridChunker()

    async def parse_all(self) -> List[dict]:
        """Load, convert, chunk and return formatted page records for all files in the uploads bucket."""
        parsed = await self._load_docs()
        if not parsed:
            return []

        records = await self._chunk_files(parsed)
        return records
    
    async def _load_docs(self) -> List[dict]:
        files = await self.supabase.strong.from_(self.bucket).list("uploads")

        if not files:
            return []

        parsed_files = []

        for file in files:
            file_name = file["name"]

            original_file_name = await self._get_original_filename(file_name)

            if file_name == ".emptyFolderPlaceholder":
                continue

            file_path = f"uploads/{file_name}"
            file_bytes = await self.supabase.storage.from_(self.bucket).download(
                file_path
            )

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

    async def _chunk_files(self, parsed_files: List[dict]):
        formatted_records = []

        for file in parsed_files:
            # parsed_files contains dicts with keys: filename, file_content
            content = file.get("file_content")
            if not content:
                continue

            # chunk the document content
            doc_chunks = self.chunker.chunk(content)

            for chunk in doc_chunks:
                # attempt to serialize the chunk (some implementations use `serialize`)
                serialize_fn = getattr(self.chunker, "serialize", None) or getattr(
                    self.chunker, "serizlize", None
                )
                if not serialize_fn:
                    # fallback to str()
                    chunk_text = str(chunk)
                else:
                    chunk_text = serialize_fn(chunk)

                page_numbers = set()

                meta = getattr(chunk, "meta", None)
                # doc_items could be stored under different attribute names depending on the chunk schema
                doc_items = None
                if meta is not None:
                    doc_items = getattr(meta, "doc_items", None) or getattr(
                        meta, "doc", None
                    )

                if doc_items:
                    # iterate safely over items and collect page numbers from provenance
                    try:
                        for item in doc_items:
                            prov = getattr(item, "prov", None) or getattr(
                                item, "provenance", None
                            )
                            if not prov:
                                continue
                            for p in prov:
                                pg = getattr(p, "page_no", None) or getattr(
                                    p, "page", None
                                )
                                if pg is not None:
                                    page_numbers.add(pg)
                    except TypeError:
                        # doc_items might be a mapping or different shape; ignore if not iterable
                        pass

                primary_page = min(page_numbers) if page_numbers else 1

                heading = None
                if meta is not None:
                    headings = getattr(meta, "headings", None) or getattr(
                        meta, "heading", None
                    )
                    if headings:
                        # headings could be a list or a single value
                        heading = (
                            headings[0]
                            if isinstance(headings, (list, tuple))
                            else headings
                        )

                formatted_records.append(
                    {
                        "filename": file.get("filename"),
                        "content": chunk_text,
                        "meta_data": {
                            "page_number": primary_page,
                            "all_spanned_pages": sorted(list(page_numbers)),
                            "heading": heading,
                        },
                    }
                )

        return formatted_records

    async def _get_original_filename(self, file_name: str) -> str:
        get_filename = select(File.original_name).where(File.stored_name == file_name)
        result = await self.db.execute(get_filename)

        original_name = result.scalar_one_or_none()

        return original_name
