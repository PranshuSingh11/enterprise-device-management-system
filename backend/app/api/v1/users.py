from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, LoginRequest
from app.services.user_service import create_user, login_user
from app.core.security import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

from app.core.authorization import require_role
from app.core.roles import Role

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=201)
def create_user_endpoint(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user_data)

@router.post("/login")
def login_endpoint(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(
        db,
        form_data.username,
        form_data.password
    )
    
@router.get("/me")
def get_current_user_endpoint(
    current_user = Depends(get_current_user)
):
    return current_user
