import os
from dotenv import load_dotenv
from fastapi import FastAPI,Request
from fastapi.responses import RedirectResponse
# from starlette.middleware.sessions import SessionMiddleware
# from fastapi.middleware.cors import CORSMiddleware

from api.routes.auth import auth_router
from api.routes.ingest import uploader_router



from core.lifespan import lifespan



load_dotenv()

app = FastAPI(lifespan=lifespan)


SECRET_KEY = os.getenv("SECRET_KEY")

app.include_router(uploader_router)
app.include_router(auth_router)



# app.add_middleware(LoggingMiddleware)

# app.add_middleware(
#     SessionMiddleware, 
#     secret_key=SECRET_KEY,
#     https_only=False,
#     max_age=3600
# )


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
        
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/")
async def main(request:Request):
    return RedirectResponse("/login")


