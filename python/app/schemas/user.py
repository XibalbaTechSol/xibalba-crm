from typing import Optional
from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    user_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_admin: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password: str
