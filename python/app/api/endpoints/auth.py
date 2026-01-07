from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.core.deps import get_db
from app.models.user import User
from app.schemas import token as token_schema

router = APIRouter()

@router.post("/login/access-token", response_model=token_schema.Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.query(User).filter(User.user_name == form_data.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not user.password:
        # Initial setup: if user exists but has no password (migration),
        # allow setting it if provided password matches a temporary default or just fail?
        # For now, let's fail.
        raise HTTPException(status_code=400, detail="User has no password set")

    if not security.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
