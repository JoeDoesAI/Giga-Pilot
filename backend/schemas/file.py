from typing import List, Optional
from pydantic import BaseModel


class FileStatus(BaseModel):
    filename: str
    success: bool
    error: Optional[str] = None


class UploadResponse(BaseModel):
    task_id: str
    status_url: str
    files_status: List[FileStatus]
