from pydantic import BaseModel, ConfigDict, Field, EmailStr
from app.core.roles import Role


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)
    role: Role


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)
    

class LoginRequest(BaseModel):
    username: str
    password: str