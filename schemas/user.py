from pydantic import BaseModel, EmailStr
from typing import Optional

from .file import FileRead


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserWithFilesRead(UserRead):
    files: list["FileRead"] = []
