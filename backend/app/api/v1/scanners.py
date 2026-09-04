from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.scanner import Scanner
from app.schemas.scanner import ScannerResponse
from app.schemas.scanner import ScannerCreate


router = APIRouter()


@router.get("/", response_model=list[ScannerResponse])
def get_scanners(db: Session = Depends(get_db)):
    return db.query(Scanner).all()

@router.post("/",response_model=ScannerResponse)
def create_scanner(scanner:ScannerCreate, db:Session = Depends(get_db)):
    new_scanner = Scanner(
        name=scanner.name,
        serial_number=scanner.serial_number,
        model=scanner.model,
        status=scanner.status,
        branch_id=scanner.branch_id
    )
    
    db.add(new_scanner)
    db.commit()
    db.refresh(new_scanner)

    return new_scanner