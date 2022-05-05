from dataclasses import dataclass


@dataclass
class InvalidError(Exception):
    message: str


@dataclass
class InvalidGameError(InvalidError):
    pass


@dataclass
class InvalidMoveError(InvalidError):
    pass
