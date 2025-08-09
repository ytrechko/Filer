from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models import File
from schemas import FileCreate, FileRead


async def create_file(file: FileCreate, db: AsyncSession) -> FileRead:
    db_file = File(title=file.title, description=file.description)
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)
    return db_file


async def read_all_files(db: AsyncSession) -> List[FileRead]:
    stmt_get = select(File)
    result = await db.execute(stmt_get)
    Files = result.scalars().all()
    return Files


async def read_file(file_id: int, db: AsyncSession) -> List[FileRead]:

    stmt_get = select(File).where(File.id == file_id)
    result = await db.execute(stmt_get)
    file = result.scalar_one_or_none()
    if not file:
        raise HTTPException(status_code=404, detail=f"File with {file_id} id not found")

    return file


async def delete_file(file_id: int, db: AsyncSession):
    stmt_availability_file = select(File).where(File.id == file_id)
    result = await db.execute(stmt_availability_file)
    availability_file = result.scalar_one_or_none()
    if not availability_file:
        raise HTTPException(status_code=404, detail=f"File with {file_id} not found")

    stmt_delete_file = delete(File).where(File.id == file_id)
    await db.execute(stmt_delete_file)
    await db.commit()
