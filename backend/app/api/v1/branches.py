from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.branch import BranchCreate, BranchResponse
from app.services.branch_service import (
    create_branch,
    get_branches,
    get_branch,
    delete_branch,
    update_branch
)

router = APIRouter()


@router.post("/", response_model=BranchResponse)
def create_branch_endpoint(
    branch: BranchCreate,
    db: Session = Depends(get_db)
):
    return create_branch(db, branch)


@router.get("/", response_model=list[BranchResponse])
def get_branches_endpoint(
    db: Session = Depends(get_db)
):
    return get_branches(db)


@router.get("/{branch_id}", response_model=BranchResponse)
def get_branch_endpoint(
    branch_id: int,
    db: Session = Depends(get_db)
):
    return get_branch(db, branch_id)

@router.put("/{branch_id}", response_model=BranchResponse)
def update_branch_endpoint(
    branch_id: int,
    branch: BranchCreate,
    db: Session = Depends(get_db)
):
    return update_branch(db, branch_id, branch)


@router.delete("/{branch_id}", response_model=BranchResponse)
def delete_branch_endpoint(
    branch_id: int,
    db: Session = Depends(get_db)
):
    return delete_branch(db, branch_id)