from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List

from models import File
from schemas import FileCreate, FileRead
from database import get_db
from crud import create_file, read_all_files, read_file, delete_file

router = APIRouter(prefix="/file", tags=["file"])


@router.post("/")
async def create_file_route(
    file: FileCreate, db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:

    return await create_file(file, db)


@router.get("/", response_model=List[FileRead])
async def read_all_files_route(db: AsyncSession = Depends(get_db)) -> List[FileRead]:
    return await read_all_files(db)


@router.get("/{file_id}/", response_model=FileRead)
async def read_file_route(file_id: int, db: AsyncSession = Depends(get_db)):
    return await read_file(file_id, db)


@router.delete("/{file_id}")
async def delete_file_route(
    file_id: int, db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    await delete_file(file_id, db)
    return {"status": "file successful deleted"}
