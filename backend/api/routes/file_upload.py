from typing import List

from fastapi import APIRouter, Request, File, UploadFile, HTTPException, Depends,status 
from api.deps.auth import get_current_user
from schemas.file import UploadResponse
from api.deps.service_deps import get_uploader,get_ingestion
from services.File.file_uploader import FileUploader
from services.Ingestion.ochestrator import IngestionOchestrator

uploader_router = APIRouter()


@uploader_router.post("/upload-docs", response_model=UploadResponse)
async def upload_docs(
    # current_user= Depends(get_current_user),
    files: List[UploadFile] = File(...),
    upload:FileUploader = Depends(get_uploader),
    ingestion:IngestionOchestrator = Depends(get_ingestion)
   
):

    # if not current_user:
    #      raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, 
    #         detail="Please Sign In"
    #     )
    
    uploader = await upload.run(files)

    # await ingestion.run()

    return uploader
