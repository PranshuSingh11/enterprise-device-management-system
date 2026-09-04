from pydantic import BaseModel


class BranchCreate(BaseModel):
    name: str
    location: str
    status: str


class BranchResponse(BaseModel):
    id: int
    name: str
    location: str
    status: str
    
    class Config:
        from_attributes = True