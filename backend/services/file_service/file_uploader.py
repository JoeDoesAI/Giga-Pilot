import uuid
from typing import List
from pathlib import Path

# from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from models.postgre.file import File

from supabase import AsyncClient

from core.config import Settings

from schemas.file import UploadResponse

class FileUploader:
    """
    save file is a class that validates and saves file to the upload folder of my app
    input a list of file objects into the run method and 

    it validates = a validators work 
        input - UploadFile
        output - List[dict] {valid,errors}

    changes the filename and stores it = create a unique file name
        input - UploadFile, db + model
        output - none

    
    saves the file to the upload folder 
        input - file 
        output - none
    """

    def __init__(self, db:AsyncSession,
                       supabase_client:AsyncClient,
                       max_size:int = 20 * 1024 * 1024,
                       allowed_extensions:List = [".pdf",".txt",".json"],
                       bucket:str = Settings.SUPABASE_BUCKET

                       ):
        self.db = db
        self.supabase_client = supabase_client
        self.max_size = max_size
        self.allowed_extensions = allowed_extensions
        self.supabase_bucket = bucket


    async def run(self, files: List[UploadFile]) -> UploadResponse:
        upload_state:List = []

        for file in files:
            validate_file = await self.validate_file(file)

            file_ext = Path(file.filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path:str = f"uploads/{unique_filename}"
            filename:str = file.filename

            if not validate_file["valid"]:
                upload_state.append({
                    "filename": filename,
                    "success": False,
                    "errors": validate_file["error"]
                })
                
                continue
            
            upload_file = await self.upload_file(file,file_path)

            if not upload_file["uploaded"]:
                upload_state.append(
                    {"filename": filename,
                    "success": False,
                    "error": upload_file["error"]}
                    )
                
                continue
            


            await self.save_file_name(filename,unique_filename)

            upload_state.append({"filename":filename,
                                "success":True,
                                })
            
        return UploadResponse(files_status = upload_state)

        
    async def validate_file(self, file:UploadFile) -> dict:

        if not file.filename or not file.filename.strip():
            return {"valid": False, "error":"no file selected"}
        

        #check file extension
        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in self.allowed_extensions:
            return {"valid": False, "error": f"The file extension {file_ext} not allowed"}
           
        #check file size
        content_size = await file.read()
        await file.seek(0)

        file_size = len(content_size)

        if file_size > self.max_size:
            return {"valid": False, "error": "Maximum file size excceded"}
        
        return {"valid": True}
    
    async def save_file_name(self,filename:str, unique_filename:str):
        new_file = File(
                        stored_name = unique_filename,
                        original_name = filename)
        
        self.db.add(new_file)

        await self.db.commit()
        # await db.refresh()


    async def upload_file(self, file:UploadFile, file_path:str) -> dict:
        try:
            
            # file.file.seek(0)

            content = await file.read()
           
            await self.supabase_client.storage.from_(self.supabase_bucket).upload(
                        path=file_path, 
                        file=content,
                        file_options={ "content-type": file.content_type, # Keeps it as PDF/Image/etc.
                                        "upsert": "true"                  # Overwrites if file exists
                                    }
                        )
            
            return{"uploaded": True}

        except Exception as e:
            return {"uploaded": False, "error": f"file was not uploaded due to {repr(e)}"}

        finally:
            file.file.close()


        


        

        

        
        

    

