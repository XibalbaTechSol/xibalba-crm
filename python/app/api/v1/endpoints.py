from fastapi import APIRouter, Depends, Body, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.controllers import metadata, i18n, record_controller
from app.api.v1 import attachment, notification
from app.core.database import get_db
from app.models.user import User

router = APIRouter()

@router.get("/")
async def get_api_index():
    return {"message": "API v1 root"}

@router.get("/App/user")
async def get_app_user(db: Session = Depends(get_db)):
    # In a real scenario, we would determine the current user from the session or token.
    # For now, since we don't have authentication middleware yet, we will fetch the first admin user
    # or a specific user to simulate a logged-in state.

    # Try to find 'admin' user or any user.
    user = db.query(User).filter(User.user_name == 'admin').first()
    if not user:
         user = db.query(User).first()

    if user:
        return {
            "user": {
                "id": user.id,
                "name": user.name,
                "username": user.user_name,
                "isAdmin": user.is_admin
            }
        }
    else:
        # Fallback if no user exists in DB yet (e.g. fresh install)
        # This is strictly for development convenience
        return {
            "user": {
                "id": "1",
                "name": "Admin",
                "username": "admin",
                "isAdmin": True
            }
        }

router.include_router(metadata.router)
router.include_router(i18n.router)
router.include_router(record_controller.router)
router.include_router(attachment.router)
router.include_router(notification.router)

# Alias for generic Entity CRUD
# Register these LAST to avoid shadowing specific routes like /Metadata
@router.get("/{entityName}")
def list_entity_alias(
    entityName: str,
    where: Optional[str] = Query(None),
    sortBy: Optional[str] = Query(None),
    asc: Optional[bool] = Query(False),
    offset: Optional[int] = Query(0),
    maxSize: Optional[int] = Query(20),
    service: record_controller.RecordService = Depends(record_controller.get_record_service)
):
    return record_controller.get_list(entityName, where, sortBy, asc, offset, maxSize, service)

@router.post("/{entityName}")
def create_entity_alias(entityName: str, data: dict = Body(...), service: record_controller.RecordService = Depends(record_controller.get_record_service)):
    return record_controller.create_record(entityName, data, service)

@router.get("/{entityName}/{id}")
def read_entity_alias(entityName: str, id: str, service: record_controller.RecordService = Depends(record_controller.get_record_service)):
    return record_controller.read_record(entityName, id, service)

@router.put("/{entityName}/{id}")
def update_entity_alias(entityName: str, id: str, data: dict = Body(...), service: record_controller.RecordService = Depends(record_controller.get_record_service)):
    return record_controller.update_record(entityName, id, data, service)

@router.delete("/{entityName}/{id}")
def delete_entity_alias(entityName: str, id: str, service: record_controller.RecordService = Depends(record_controller.get_record_service)):
    return record_controller.delete_record(entityName, id, service)
