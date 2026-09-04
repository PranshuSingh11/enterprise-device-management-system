from pydantic import BaseModel


class ScannerCreate(BaseModel):
    name: str
    serial_number: str
    model: str
    status: str
    branch_id: int


class ScannerResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    model: str
    status: str
    branch_id: int
    
    class Config:
        from_attributes = True