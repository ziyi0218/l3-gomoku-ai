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
            "Black has a longer local chain that can be extended, while another "
            "central shape has more open development space."
        ),
        purpose=(
            "Test whether updated Eval A still favors immediate local extension, "
            "while Eval B/C may value openness or window potential."
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
            "A blocked longer line appears near an open central shape."
        ),
        purpose=(
            "Highlight the difference between length-based scoring and open-end "
            "shape scoring."
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
        name="E3_window_potential",
        description=(
            "One central point participates in several possible five-cell windows, "
            "while another point extends a visible local pattern."
        ),
        purpose=(
            "Give Eval C a chance to prefer multi-window potential over local "
            "segment length."
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
            "White has a developing diagonal threat while Black has a tempting "
            "horizontal attacking option."
        ),
        purpose=(
            "Observe whether evaluations attack, defend, or reduce opponent window "
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
        name="E5_center_space",
        description=(
            "A local edge-side chain competes with central development points that "
            "can expand in multiple directions."
        ),
        purpose=(
            "Check whether Eval C's window/space view prefers central development "
            "over local extension."
        ),
        player_to_move=1,
        moves=[
            (4, 3, 1),
            (4, 4, 1),
            (4, 5, 1),
            (4, 2, -1),
            (7, 7, 1),
            (7, 9, -1),
            (8, 8, 1),
            (6, 8, -1),
            (9, 7, -1),
        ],
    ),
    EvaluationPosition(
        name="E6_complex_midgame",
        description=(
            "Both players have several two- and three-stone patterns in a compact "
            "midgame cluster."
        ),
        purpose=(
            "Compare behavior, cost, nodes, and cutoffs in a moderate midgame."
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
