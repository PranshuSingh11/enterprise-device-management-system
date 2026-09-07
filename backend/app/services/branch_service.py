from sqlalchemy.orm import Session

from app.models.branch import Branch
from app.schemas.branch import BranchCreate

from fastapi import HTTPException


def create_branch(db: Session, branch_data: BranchCreate):
    new_branch = Branch(
        name=branch_data.name,
        location=branch_data.location,
        status=branch_data.status
    )

    db.add(new_branch)
    db.commit()
    db.refresh(new_branch)

    return new_branch


def get_branches(db: Session):
    return db.query(Branch).all()


def get_branch(db: Session, branch_id: int):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()

    if not branch:
        raise HTTPException(
            status_code=404,
            detail="Branch not found"
        )

    return branch

def update_branch(
    db: Session,
    branch_id: int,
    branch_data: BranchCreate
):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()

    if not branch:
        raise HTTPException(
            status_code=404,
            detail="Branch not found"
        )

    branch.name = branch_data.name
    branch.location = branch_data.location
    branch.status = branch_data.status

    db.commit()
    db.refresh(branch)

    return branch


def delete_branch(db: Session, branch_id: int):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()

    if not branch:
        raise HTTPException(
            status_code=404,
            detail="Branch not found"
        )

    db.delete(branch)
    db.commit()

    return branch