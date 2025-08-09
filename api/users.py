from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List

from schemas import UserCreate, UserRead, UserUpdate, UserWithFilesRead
from database import get_db
from crud import create_user, read_user, read_all_users, update_user, delete_user


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/")
async def create_user_route(
    user: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserWithFilesRead:
    return await create_user(user, db)


@router.get("/{user_id}/", response_model=UserWithFilesRead)
async def read_user_route(
    user_id: int, db: AsyncSession = Depends(get_db)
) -> UserWithFilesRead:
    return await read_user(user_id, db)


@router.get("/", response_model=List[UserWithFilesRead])
async def read_all_users_route(
    db: AsyncSession = Depends(get_db),
) -> List[UserWithFilesRead]:
    return await read_all_users(db)


@router.put("/{user_id}/")
async def update_user_route(
    user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)
) -> UserWithFilesRead:
    return await update_user(user_id, user, db)


@router.delete("/{user_id}/")
async def delete_user_route(
    user_id: int, db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    await delete_user(user_id, db)
    return {"status": "user successful deleted"}
