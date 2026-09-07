from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.scanner import Scanner
from app.schemas.scanner import ScannerCreate

from fastapi import HTTPException

def get_scanners(db: Session):
    return db.query(Scanner).all()


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

    try:
        db.add(new_scanner)
        db.commit()
        db.refresh(new_scanner)

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