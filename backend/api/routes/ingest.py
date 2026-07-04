from typing import List

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from celery.result import AsyncResult

from api.deps.auth import get_current_user, get_current_admin_user
from api.deps.service import get_uploader
from celery_app import celery_app
from services.file.upload import FileUploader
from services.ingest.tasks import ingest_files
from schemas.file import UploadResponse
from schemas.ingest import IngestionTaskStatusResponse

uploader_router = APIRouter(tags=["ingestion"])


@uploader_router.post("/upload-docs", response_model=UploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_docs(
    current_user=Depends(get_current_user),
    files: List[UploadFile] = File(...),
    upload: FileUploader = Depends(get_uploader),
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to upload documents",
        )

    upload_result = await upload.run(files)
    celery_task = ingest_files.apply_async()

    return UploadResponse(
        task_id=celery_task.id,
        status_url=f"/ingest/admin/ingestion-status/{celery_task.id}",
        files_status=upload_result["files_status"],
    )


@uploader_router.get(
    "/ingest/admin/ingestion-status/{task_id}",
    response_model=IngestionTaskStatusResponse,
)
async def ingestion_status(
    task_id: str,
    current_user=Depends(get_current_admin_user),
):
    async_result = AsyncResult(task_id, app=celery_app)
    status_name = async_result.status
    ready_flag = async_result.ready()
    result_value = None
    error_message = None

    if ready_flag:
        try:
            result_value = async_result.get(timeout=1)
        except Exception as exc:
            error_message = str(exc)

    return IngestionTaskStatusResponse(
        task_id=task_id,
        status=status_name,
        ready=ready_flag,
        result=result_value,
        error=error_message,
    )

