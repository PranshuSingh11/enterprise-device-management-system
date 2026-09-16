from sqlalchemy.orm import Session
from sqlalchemy import or_
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


def get_branches(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
    status: str | None = None,
    sort_by: str = "id",
    sort_order: str = "asc"
):
    query = db.query(Branch)

    if search:
        search_term = f"%{search}%"

        query = query.filter(
            or_(
                Branch.name.ilike(search_term),
                Branch.location.ilike(search_term)
            )
        )

    if status:
        query = query.filter(Branch.status == status)

    ALLOWED_SORT_FIELDS = {
    "id",
    "name",
    "location",
    "status"
    }

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

    sort_column = getattr(Branch, sort_by, Branch.id)

    total = query.count()

    if sort_order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    

    offset = (page - 1) * page_size

    branches = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    total_pages = (total + page_size - 1) // page_size

    return {
        "items": branches,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages
    }


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