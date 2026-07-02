from pydantic import BaseModel,EmailStr,Field
from typing import Optional


class UserCreate(BaseModel):
    firstname: str = Field(..., min_length=3, max_length=50)
    lastname: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    # Optional role - default is 'user'. Use 'admin' for admin accounts (requires ACCESS_CODE).
    role: Optional[str] = "user"
    # Optional admin access code for creating admin accounts
    access_code: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str


