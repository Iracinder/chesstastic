from fastapi import APIRouter, File, UploadFile

from utils.dependencies import COURSE_LOCATION

router = APIRouter(prefix="/pgns")


@router.get("/")
async def list_pgn():
    return [pgn.stem for pgn in COURSE_LOCATION.glob('*.pgn')]


@router.post("/")
async def create_pgns(files: list[UploadFile] = File(...)):
    file_uploaded = []
    for file in files:
        content = await file.read()
        (COURSE_LOCATION / file.filename).write_bytes(content)
        file_uploaded.append(file.filename)
    return file_uploaded
