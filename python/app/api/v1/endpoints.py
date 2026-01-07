from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers import metadata, i18n, record_controller
from app.api.v1 import attachment, notification
from app.api.endpoints import auth
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

# Public auth routes
router.include_router(auth.router)

@router.get("/")
async def get_api_index():
    return {"message": "API v1 root"}

@router.get("/App/user")
async def get_app_user(current_user: User = Depends(get_current_user)):
    # Uses the dependency injected user from the token
    return {
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "username": current_user.user_name,
            "isAdmin": current_user.is_admin
        }
    }

router.include_router(metadata.router)
router.include_router(i18n.router)
router.include_router(record_controller.router)
router.include_router(attachment.router)
router.include_router(notification.router)
