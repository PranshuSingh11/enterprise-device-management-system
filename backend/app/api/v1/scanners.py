from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.scanner import Scanner
from app.schemas.scanner import ScannerResponse
from app.schemas.scanner import ScannerCreate
from app.services.scanner_service import create_scanner
from app.services.scanner_service import get_scanner
from app.services.scanner_service import get_scanners
from app.services.scanner_service import update_scanner
from app.services.scanner_service import delete_scanner

from app.core.authorization import require_role
from app.core.roles import Role


router = APIRouter()


@router.get("/", response_model=list[ScannerResponse])
def get_scanners_endpoint(
    current_user=Depends(require_role(
        Role.ADMIN,
        Role.MANAGER,
        Role.VIEWER
    )),
    db: Session = Depends(get_db)
):
    return get_scanners(db)

@router.get("/{scanner_id}", response_model=ScannerResponse)
def get_scanner_endpoint(
    scanner_id: int,
    current_user=Depends(require_role(
            Role.ADMIN,
            Role.MANAGER,
            Role.VIEWER
        )),
    db: Session = Depends(get_db)
):
    return get_scanner(db, scanner_id)

@router.post("/",response_model=ScannerResponse)
def create_scanner_endpoint(
    scanner: ScannerCreate,
    current_user=Depends(require_role(
            Role.ADMIN,
            Role.MANAGER,
        )),
    db: Session = Depends(get_db)
):
    return create_scanner(db, scanner)

@router.put("/{scanner_id}", response_model=ScannerResponse)
def update_scanner_endpoint(
    scanner_id: int,
    scanner: ScannerCreate,
    current_user=Depends(require_role(
            Role.ADMIN,
            Role.MANAGER,
        )),
    db: Session = Depends(get_db)
):
    return update_scanner(db, scanner_id, scanner)

@router.delete("/{scanner_id}", response_model=ScannerResponse)
def update_scanner_endpoint(
    scanner_id: int,
    current_user=Depends(require_role(
            Role.ADMIN,
        )),
    db: Session = Depends(get_db)
):
    return delete_scanner(db, scanner_id)