from dataclasses import dataclass
from typing import List, Tuple

from game.board import Board

MoveRecord = Tuple[int, int, int]


@dataclass(frozen=True)
class EvaluationPosition:
    name: str
    description: str
    purpose: str
    player_to_move: int
    moves: List[MoveRecord]

    def make_board(self) -> Board:
        board = Board(15)
        for r, c, player in self.moves:
            if not board.place(r, c, player):
                raise ValueError(f"Invalid move in {self.name}: {(r, c, player)}")
        return board


EVALUATION_POSITIONS = [
    EvaluationPosition(
        name="E1_length_pressure",
        description=(
            "Black has a longer one-sided segment and a shorter central shape with "
            "more open development space."
        ),
        purpose=(
            "Eval A may prefer extending the longer local chain, while Eval B/C can "
            "value openness or future windows."
        ),
        player_to_move=1,
        moves=[
            (7, 5, -1),
            (7, 6, 1),
            (7, 7, 1),
            (7, 8, 1),
            (8, 7, -1),
            (9, 7, 1),
            (9, 8, 1),
            (6, 8, -1),
            (8, 9, -1),
        ],
    ),
    EvaluationPosition(
        name="E2_open_vs_blocked",
        description=(
            "A blocked longer line competes with an open three shape in the same "
            "central area."
        ),
        purpose=(
            "Show whether open-end evaluation avoids overvaluing blocked length."
        ),
        player_to_move=1,
        moves=[
            (6, 5, -1),
            (6, 6, 1),
            (6, 7, 1),
            (6, 8, 1),
            (6, 9, -1),
            (8, 6, 1),
            (8, 7, 1),
            (8, 8, 1),
            (7, 8, -1),
            (9, 8, -1),
        ],
    ),
    EvaluationPosition(
        name="E3_window_cross",
        description=(
            "One central intersection contributes to several potential five-cell "
            "windows, while another move extends a visible local shape."
        ),
        purpose=(
            "Check whether Eval C favors multi-window potential over local length."
        ),
        player_to_move=1,
        moves=[
            (7, 7, 1),
            (7, 9, 1),
            (6, 8, 1),
            (8, 8, -1),
            (9, 7, -1),
            (8, 6, 1),
            (8, 7, 1),
            (6, 6, -1),
            (6, 10, -1),
            (9, 9, -1),
        ],
    ),
    EvaluationPosition(
        name="E4_attack_defense",
        description=(
            "White has a growing diagonal threat, while Black has a horizontal "
            "attacking option."
        ),
        purpose=(
            "Observe whether evaluations prefer attacking or reducing opponent "
            "potential."
        ),
        player_to_move=1,
        moves=[
            (7, 7, -1),
            (8, 8, -1),
            (9, 9, -1),
            (6, 7, 1),
            (6, 8, 1),
            (6, 9, 1),
            (7, 9, 1),
            (8, 7, -1),
            (9, 7, 1),
            (5, 8, -1),
        ],
    ),
    EvaluationPosition(
        name="E5_complex_midgame",
        description=(
            "Both players have several two- and three-stone patterns in a compact "
            "midgame cluster."
        ),
        purpose=(
            "Compare evaluation choices, cost, and pruning in a denser but still "
            "bounded candidate space."
        ),
        player_to_move=1,
        moves=[
            (7, 7, 1),
            (7, 8, -1),
            (8, 7, 1),
            (6, 7, -1),
            (8, 8, 1),
            (6, 8, -1),
            (9, 7, 1),
            (5, 8, -1),
            (8, 6, 1),
            (6, 9, -1),
            (9, 8, 1),
            (5, 7, -1),
        ],
    ),
]
