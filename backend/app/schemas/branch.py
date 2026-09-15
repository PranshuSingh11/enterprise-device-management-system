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
        
class BranchListResponse(BaseModel):
    items: list[BranchResponse]
    page: int
    page_size: int
    total: int
    total_pages: int