from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.branch import Branch
from app.schemas.branch import BranchResponse
from app.schemas.branch import BranchCreate

router = APIRouter()


@router.post("/",response_model=BranchResponse)
def create_branch(
    branch:BranchCreate,
    db: Session = Depends(get_db)
):
    new_branch = Branch(
        name=branch.name,
        location=branch.location,
        status=branch.status
    )

    db.add(new_branch)
    db.commit()
    db.refresh(new_branch)

    return new_branch