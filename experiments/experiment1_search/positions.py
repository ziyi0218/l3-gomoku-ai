from dataclasses import dataclass
from typing import List, Tuple

from game.board import Board

MoveRecord = Tuple[int, int, int]


@dataclass(frozen=True)
class FixedPosition:
    name: str
    moves: List[MoveRecord]
    player_to_move: int
    description: str
    expected_property: str

    def make_board(self) -> Board:
        board = Board(15)
        for r, c, player in self.moves:
            placed = board.place(r, c, player)
            if not placed:
                raise ValueError(f"Invalid fixed position move: {(r, c, player)}")
        return board


FIXED_POSITIONS = [
    FixedPosition(
        name="P1_opening",
        moves=[
            (7, 7, 1),
            (7, 8, -1),
            (8, 7, 1),
            (6, 7, -1),
        ],
        player_to_move=1,
        description="Opening position with a small central cluster.",
        expected_property="Low branching factor; all algorithms should agree quickly.",
    ),
    FixedPosition(
        name="P2_midgame",
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
        description="Balanced midgame with both sides occupying the center area.",
        expected_property="Moderate branching factor and no immediate forced win.",
    ),
    FixedPosition(
        name="P3_single_threat",
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
        description="Black has a three-stone horizontal threat.",
        expected_property="Search should prioritize extending or converting the threat.",
    ),
    FixedPosition(
        name="P4_mutual_threats",
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
        description="Both players have visible threats near the center.",
        expected_property="Good position for checking score equivalence under pressure.",
    ),
    FixedPosition(
        name="P5_complex_midgame",
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
        description="Denser midgame cluster with more candidate moves.",
        expected_property="Useful for observing larger node reductions at depth 3.",
    ),
]
