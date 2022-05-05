import os
from pathlib import Path

import chess
from chess.pgn import Game
from pydantic import BaseModel

COURSE_LOCATION = Path(os.environ['COURSE_LOCATION'])
COURSES: dict[str, Game] = {course.stem: chess.pgn.read_game(course.open()) for course in
                            COURSE_LOCATION.glob("**/*.pgn")}


class MoveRequest(BaseModel):
    courses: list[str]
    move_history: list[str]
    origin: int
    to: int


class Move(BaseModel):
    fen: str
    san: str
    uci: str


class BoardState(BaseModel):
    move_history: list[Move]
    selected_pgns: list[str]


class MoveError(BaseModel):
    comment: str
    possible_variations: list[dict[str, int]]


class MoveVariation(BaseModel):
    course: str
    move_history: list[Move]
    FEN: str | None = None
    error: MoveError | None = None
