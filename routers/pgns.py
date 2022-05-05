from fastapi import APIRouter, File, UploadFile

from utils.dependencies import COURSE_LOCATION

router = APIRouter(prefix="/pgns")


@router.get("/")
async def list_pgn():
    return [{"value": pgn.stem, "label": pgn.stem} for pgn in COURSE_LOCATION.glob('*.pgn')]


@router.post("/")
async def create_pgn(file: UploadFile = File(...)):
    content = await file.read()
    (COURSE_LOCATION / file.filename).write_bytes(content)
    return {"filename": file.filename}
