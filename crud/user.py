from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from typing import List

from schemas import UserCreate, UserRead, UserUpdate, UserWithFilesRead
from models import User


async def create_user(user: UserCreate, db: AsyncSession) -> UserWithFilesRead:
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def read_user(user_id: int, db: AsyncSession) -> UserWithFilesRead:
    stmt = select(User).options(joinedload(User.files)).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with {user_id} id not found")

    return user


async def read_all_users(db: AsyncSession) -> List[UserWithFilesRead]:
    stmt = select(User).options(joinedload(User.files))
    result = await db.execute(stmt)
    users = result.unique().scalars().all()

    return users


async def update_user(
    user_id: int, user: UserUpdate, db: AsyncSession
) -> UserWithFilesRead:
    check_stmt = select(User).where(User.id == user_id)
    result = await db.execute(check_stmt)
    availability_user = result.scalar_one_or_none()
    if not availability_user:
        raise HTTPException(
            status_code=404, detail=f"User with {user_id} id is not found"
        )

    update_stmt = (
        update(User)
        .where(User.id == user_id)
        .values(**user.model_dump(exclude_unset=True))
    )
    await db.execute(update_stmt)
    await db.commit()

    select_stmt = select(User).options(joinedload(User.files)).where(User.id == user_id)
    result = await db.execute(select_stmt)
    updated_user = result.scalars().first()
    return updated_user


async def delete_user(user_id: int, db: AsyncSession):
    stmt_availability_user = select(User).where(User.id == user_id)
    result = await db.execute(stmt_availability_user)
    availability_user = result.scalar_one_or_none()
    if not availability_user:
        raise HTTPException(status_code=404, detail=f"User with {user_id} id not found")

    stmt_delete_user = delete(User).where(User.id == user_id)
    await db.execute(stmt_delete_user)

    await db.commit()
