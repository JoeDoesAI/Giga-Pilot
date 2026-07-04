# from fastapi import APIRouter, Request, Depends, HTTPException, status
# from fastapi.responses import StreamingResponse

# from api.deps.auth import get_current_user
# from schemas.qa import QA_Response
# from backend.services.retrival.ochestrator import RetrivalOchestrator

# from api.deps.service import get_query_ans
# qa_router = APIRouter()

# @qa_router.post("/query",response_model=QA_Response)
# async def answer_prompt(request:Request,
#                         user_query: str,
#                         current_user:str = Depends(get_current_user),
#                         answer:RetrivalOchestrator = Depends(get_query_ans)):
#     if not current_user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, 
#             detail="validation error"
#         )
    
#     generator = answer.run(user_query)

#     return StreamingResponse(generator, media_type="text/plain")


