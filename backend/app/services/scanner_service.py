from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.scanner import Scanner
from app.models.branch import Branch
from app.schemas.scanner import ScannerCreate
from sqlalchemy import or_
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

ALLOWED_SORT_FIELDS = {
    "id",
    "name",
    "serial_number",
    "model",
    "status",
    "branch_id"
}

def get_scanners(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
    status: str | None = None,
    branch_id: int | None = None,
    sort_by: str = "id",
    sort_order: str = "asc"
):
    offset = (page - 1) * page_size

    query = db.query(Scanner)
    
    if search:
        search_term = f"%{search}%"

        query = query.filter(
            or_(
                Scanner.name.ilike(search_term),
                Scanner.serial_number.ilike(search_term),
                Scanner.model.ilike(search_term)
            )
        )
    
    if status:
        query = query.filter(Scanner.status == status)

    if branch_id:
        query = query.filter(Scanner.branch_id == branch_id)
        
    if sort_by not in ALLOWED_SORT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field: {sort_by}"
        )

    if sort_order.lower() not in {"asc", "desc"}:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort order: {sort_order}"
        )
        
    sort_column = getattr(Scanner, sort_by, Scanner.id)
    
    total = query.count()

    if sort_order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    

    scanners = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    total_pages = (total + page_size - 1) // page_size

    return {
        "items": scanners,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages
    }


def get_scanner(db: Session, scanner_id: int):
    scanner = db.query(Scanner).filter(Scanner.id == scanner_id).first()

    if not scanner:
        raise HTTPException(
            status_code=404,
            detail="Scanner not found"
        )

    return scanner


def create_scanner(db: Session, scanner_data: ScannerCreate):
    new_scanner = Scanner(
        name=scanner_data.name,
        serial_number=scanner_data.serial_number,
        model=scanner_data.model,
        status=scanner_data.status,
        branch_id=scanner_data.branch_id
    )
    
    branch = db.query(Branch).filter(
    Branch.id == scanner_data.branch_id
).first()

    if not branch:
        raise HTTPException(
            status_code=404,
            detail="Branch not found"
        )

    try:
        db.add(new_scanner)
        db.commit()
        db.refresh(new_scanner)
        
        logger.info(
        "Scanner '%s' created successfully",
        new_scanner.name
    )

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Scanner with this serial number already exists"
        )

    return new_scanner

def update_scanner(
    db: Session,
    scanner_id: int,
    scanner_data: ScannerCreate
):
    scanner = db.query(Scanner).filter(Scanner.id == scanner_id).first()

    if not scanner:
        raise HTTPException(
            status_code=404,
            detail="Scanner not found"
        )

    scanner.name = scanner_data.name
    scanner.serial_number = scanner_data.serial_number
    scanner.model = scanner_data.model
    scanner.status = scanner_data.status
    scanner.branch_id = scanner_data.branch_id

    db.commit()
    db.refresh(scanner)

    return scanner

def delete_scanner(db: Session, scanner_id: int):
    scanner = db.query(Scanner).filter(Scanner.id == scanner_id).first()

    if not scanner:
        raise HTTPException(
            status_code=404,
            detail="Scanner not found"
        )

    db.delete(scanner)
    db.commit()

    return scanner