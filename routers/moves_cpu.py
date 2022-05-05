import random

import chess
from chess.pgn import ChildNode, Game
from fastapi import APIRouter, HTTPException

from utils.dependencies import Move, BoardState, MoveVariation, COURSES
from utils.errors import InvalidError, InvalidMoveError, InvalidGameError

router = APIRouter(prefix="/cpu")


def move_from_variation(board: chess.Board, variation: ChildNode) -> Move:
    return Move(fen=board.fen(), uci=variation.uci(), san=variation.san())


def possible_variation(course: str, game: ChildNode, board_state: BoardState) -> list[MoveVariation]:
    return [MoveVariation(course=course,
                          move_history=[*board_state.move_history, move_from_variation(variation.board(), variation)],
                          FEN=variation.board().fen())
            for variation in game.variations]


def progress_game_history(game: Game, move_history: list[Move]) -> ChildNode:
    """Makes sure that the current history of moves is valid and return the board after that sequence of moves."""
    game = game.root()
    for move in move_history:
        try:
            game = game.variation(chess.Move.from_uci(move.uci))
        except KeyError:
            raise InvalidGameError(message=f"Invalid move played {chess.Move.from_uci(move.uci)}.")
        except ValueError:
            raise InvalidGameError(message=f"Invalid uci notation {move}")
    return game


async def list_possible_next_move(course_name: str, board_state: BoardState) -> list[MoveVariation]:
    course_pgn = COURSES[course_name]
    game = progress_game_history(course_pgn, board_state.move_history)
    return possible_variation(course_name, game, board_state)


# Routes
@router.post('/move', response_model=MoveVariation)
async def cpu_move_request(board_state: BoardState):
    choices: list[MoveVariation] = []
    exceptions: list[InvalidError] = []
    for course in board_state.selected_pgns:
        try:
            choices += await list_possible_next_move(course, board_state)
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Couldn't find a course with name {course}.")
        except (InvalidMoveError, InvalidGameError) as e:
            exceptions.append(e)

    if len(choices) == 0:
        raise HTTPException(status_code=400, detail='\n'.join([e.message for e in exceptions]))
    if len(posssibilies := [choice for choice in choices if choice.error is None]):
        return random.choice(posssibilies)
    else:
        return choices[0]
