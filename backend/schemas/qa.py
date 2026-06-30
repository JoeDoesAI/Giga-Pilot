from pydantic import BaseModel

class QA_Response(BaseModel):
    prompt_response: str
    citation: str

class MessageRole(BaseModel):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"