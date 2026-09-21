from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.branch import BranchCreate, BranchResponse, BranchListResponse
from app.services.branch_service import (
    create_branch,
    get_branches,
    get_branch,
    delete_branch,
    update_branch
)
from app.core.authorization import require_role
from app.core.roles import Role
from fastapi import APIRouter, Depends, Query

router = APIRouter()


@router.post("/", response_model=BranchResponse,status_code=201)
def create_branch_endpoint(
    branch: BranchCreate,
        current_user=Depends(require_role(
        Role.ADMIN,
        Role.MANAGER,
    )),
    db: Session = Depends(get_db)
):
    return create_branch(db, branch)


@router.get("/", response_model=BranchListResponse)
def get_branches_endpoint(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    status: str | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    current_user=Depends(require_role(
        Role.ADMIN,
        Role.MANAGER,
        Role.VIEWER
    )),
    db: Session = Depends(get_db)
):
    return get_branches(db,page=page,
        page_size=page_size,
        search=search,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order)


@router.get("/{branch_id}", response_model=BranchResponse)
def get_branch_endpoint(
    branch_id: int,
    current_user=Depends(require_role(
        Role.ADMIN,
        Role.MANAGER,
        Role.VIEWER
    )),
    db: Session = Depends(get_db)
):
    return get_branch(db, branch_id)

@router.put("/{branch_id}", response_model=BranchResponse)
def update_branch_endpoint(
    branch_id: int,
    branch: BranchCreate,
    current_user=Depends(require_role(
        Role.ADMIN,
        Role.MANAGER
    )),
    db: Session = Depends(get_db)
):
    return update_branch(db, branch_id, branch)


@router.delete("/{branch_id}", response_model=BranchResponse)
def delete_branch_endpoint(
    branch_id: int,
    current_user=Depends(require_role(
        Role.ADMIN,
    )),
    db: Session = Depends(get_db)
):
    return delete_branch(db, branch_id)