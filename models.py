from dataclasses import dataclass
from typing import Callable, Optional, Tuple

from game.board import Board

Move = Tuple[int, int]
EvalFn = Callable[[Board, int], float]


@dataclass
class MoveStats:
    time_seconds: float
    nodes: int


@dataclass
class GameResult:
    winner: Optional[int]
    moves: int
    total_time: float

    black_depth: int
    white_depth: int

    black_eval_name: str
    white_eval_name: str

    black_avg_time: float
    white_avg_time: float

    black_avg_nodes: float
    white_avg_nodes: float
