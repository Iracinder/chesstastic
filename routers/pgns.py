import chess.pgn
from fastapi import APIRouter, File, UploadFile, HTTPException

from utils.dependencies import COURSE_LOCATION

router = APIRouter(prefix="/pgns")


@router.get("/")
async def list_pgn():
    return [pgn.stem for pgn in COURSE_LOCATION.glob('*.pgn')]


@router.post("/")
async def create_pgns(files: list[UploadFile] = File(...)):
    file_uploaded = []
    failed_upload = []
    for file in files:
        content = await file.read()
        new_pgn = COURSE_LOCATION / file.filename
        new_pgn.write_bytes(content)
        try:
            with new_pgn.open() as f:
                chess.pgn.read_game(f)
                file_uploaded.append(file.filename)
        except Exception:
            new_pgn.unlink()
            failed_upload.append(file.filename)
    return {'uploaded': file_uploaded, 'failed': failed_upload}
