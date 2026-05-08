from dataclasses import dataclass
from typing import List, Tuple

from game.board import Board

MoveRecord = Tuple[int, int, int]


@dataclass(frozen=True)
class OpeningPosition:
    name: str
    moves: List[MoveRecord]
    player_to_move: int
    description: str

    def make_board(self) -> Board:
        board = Board(15)
        for r, c, player in self.moves:
            if not board.place(r, c, player):
                raise ValueError(f"Invalid opening move in {self.name}: {(r, c, player)}")
        return board


OPENING_POSITIONS = [
    OpeningPosition(
        name="O1_small_center",
        moves=[
            (7, 7, 1),
            (7, 8, -1),
            (8, 7, 1),
            (6, 7, -1),
        ],
        player_to_move=1,
        description="Small central opening cluster.",
    ),
    OpeningPosition(
        name="O2_balanced_mid",
        moves=[
            (7, 7, 1),
            (7, 8, -1),
            (8, 7, 1),
            (6, 7, -1),
            (8, 8, 1),
            (6, 8, -1),
            (9, 7, 1),
            (5, 8, -1),
        ],
        player_to_move=1,
        description="Balanced midgame opening around the center.",
    ),
    OpeningPosition(
        name="O3_single_threat",
        moves=[
            (7, 6, 1),
            (6, 7, -1),
            (7, 7, 1),
            (8, 8, -1),
            (7, 8, 1),
            (6, 8, -1),
            (5, 6, 1),
            (8, 7, -1),
        ],
        player_to_move=1,
        description="Black has a visible local horizontal threat.",
    ),
    OpeningPosition(
        name="O4_mutual_threats",
        moves=[
            (7, 5, 1),
            (6, 7, -1),
            (7, 6, 1),
            (7, 7, -1),
            (7, 8, 1),
            (8, 7, -1),
            (5, 5, 1),
            (9, 7, -1),
            (6, 6, 1),
            (8, 8, -1),
        ],
        player_to_move=1,
        description="Both players already have local tactical pressure.",
    ),
    OpeningPosition(
        name="O5_dense_center",
        moves=[
            (7, 7, 1),
            (7, 8, -1),
            (8, 7, 1),
            (6, 7, -1),
            (8, 8, 1),
            (6, 8, -1),
            (9, 7, 1),
            (5, 8, -1),
            (9, 8, 1),
            (5, 7, -1),
            (8, 6, 1),
            (6, 9, -1),
            (10, 7, 1),
            (4, 8, -1),
        ],
        player_to_move=1,
        description="Denser central opening with a wider candidate set.",
    ),
]