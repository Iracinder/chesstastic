from typing import Optional

import chess
from fastapi import APIRouter

router = APIRouter(prefix="/player")


@router.get("/possible_moves")
async def possible_moves(fen: str, square: Optional[int] = None):
    """List all possible move for selected piece based on current fen and selected square"""
    board = chess.Board(fen=fen)
    return [move.to_square
            for move in board.legal_moves
            if move.from_square == square] if square is not None else board.legal_moves


@router.get("/move")
async def move(fen: str, from_square: int, to_square: int):
    """Return the state of the new board after player has moved"""
    board = chess.Board(fen=fen)
    new_move = chess.Move(from_square=from_square, to_square=to_square)
    fullmove_number = board.fullmove_number
    san = board.san_and_push(new_move)
    return {'fen': board.fen(), 'uci': new_move.uci(), 'san': san, 'move_number': fullmove_number}
