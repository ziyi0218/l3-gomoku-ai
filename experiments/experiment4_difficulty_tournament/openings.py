from dataclasses import dataclass
from typing import List, Tuple

from game.board import Board

MoveRecord = Tuple[int, int, int]
BOARD_SIZE = 15


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


def mirror_columns(moves: List[MoveRecord]) -> List[MoveRecord]:
    return [(r, BOARD_SIZE - 1 - c, player) for r, c, player in moves]


def swap_players(moves: List[MoveRecord]) -> List[MoveRecord]:
    return [(r, c, -player) for r, c, player in moves]


M1_CENTRAL_CROSS = [
    (7, 7, 1),
    (7, 8, -1),
    (8, 7, 1),
    (6, 7, -1),
    (8, 8, 1),
    (6, 8, -1),
    (7, 6, 1),
    (8, 6, -1),
]

M1_CENTRAL_CROSS_VARIANT = [
    (7, 7, 1),
    (7, 8, -1),
    (8, 7, 1),
    (6, 7, -1),
    (8, 8, 1),
    (6, 8, -1),
    (7, 6, 1),
    (8, 6, -1),
    (6, 9, 1),
    (9, 7, -1),
]

M2_OFFSET_TENSION = [
    (7, 7, 1),
    (7, 8, -1),
    (8, 8, 1),
    (6, 8, -1),
    (8, 6, 1),
    (6, 7, -1),
    (9, 7, 1),
    (7, 5, -1),
    (5, 8, 1),
]

M3_DIAGONAL_BALANCE = [
    (7, 7, 1),
    (8, 8, -1),
    (6, 6, 1),
    (7, 8, -1),
    (8, 6, 1),
    (6, 8, -1),
    (9, 7, 1),
    (5, 7, -1),
]

M3_DIAGONAL_BALANCE_VARIANT = [
    (7, 7, 1),
    (8, 8, -1),
    (6, 6, 1),
    (7, 8, -1),
    (8, 6, 1),
    (6, 8, -1),
    (9, 7, 1),
    (5, 7, -1),
    (7, 5, 1),
    (8, 9, -1),
]

M4_WIDE_CENTER = [
    (7, 7, 1),
    (7, 9, -1),
    (8, 8, 1),
    (6, 8, -1),
    (8, 6, 1),
    (6, 6, -1),
    (9, 7, 1),
    (5, 8, -1),
    (7, 5, 1),
]

M4_WIDE_CENTER_VARIANT = [
    (7, 7, 1),
    (7, 9, -1),
    (8, 8, 1),
    (6, 8, -1),
    (8, 6, 1),
    (6, 6, -1),
    (9, 7, 1),
    (5, 8, -1),
    (7, 5, 1),
    (8, 10, -1),
]

M5_SIDE_EXPANSION = [
    (6, 6, 1),
    (6, 7, -1),
    (7, 6, 1),
    (7, 8, -1),
    (8, 7, 1),
    (5, 7, -1),
    (9, 8, 1),
    (8, 5, -1),
]

M2_OFFSET_TENSION_MIRROR = mirror_columns(M2_OFFSET_TENSION)
M2_OFFSET_TENSION_MIRROR_VARIANT = [
    (7, 7, 1),
    (7, 6, -1),
    (8, 6, 1),
    (6, 6, -1),
    (8, 8, 1),
    (6, 7, -1),
    (9, 7, 1),
    (7, 9, -1),
    (5, 6, 1),
    (9, 5, -1),
]


OPENING_POSITIONS = [
    OpeningPosition(
        name="O1_central_cross_black",
        moves=M1_CENTRAL_CROSS,
        player_to_move=1,
        description="Balanced central cluster with no immediate forcing line, Black to move.",
    ),
    OpeningPosition(
        name="O2_central_cross_variant_white",
        moves=swap_players(M1_CENTRAL_CROSS_VARIANT),
        player_to_move=-1,
        description="Expanded central-cross family with extra central stones, White to move.",
    ),
    OpeningPosition(
        name="O3_wide_center_variant_black",
        moves=M4_WIDE_CENTER_VARIANT,
        player_to_move=1,
        description="Wide-center family with one extra remote stone, Black to move.",
    ),
    OpeningPosition(
        name="O4_wide_center_white",
        moves=M4_WIDE_CENTER,
        player_to_move=-1,
        description="Wider central spread that rewards planning over tactics, White to move.",
    ),
    OpeningPosition(
        name="O5_offset_tension_mirror_variant_black",
        moves=M2_OFFSET_TENSION_MIRROR_VARIANT,
        player_to_move=1,
        description="Expanded mirrored offset-tension family, Black to move.",
    ),
    OpeningPosition(
        name="O6_diagonal_balance_variant_white",
        moves=swap_players(M3_DIAGONAL_BALANCE_VARIANT),
        player_to_move=-1,
        description="Expanded diagonal-balance family, White to move.",
    ),
    OpeningPosition(
        name="O7_offset_tension_mirror_black",
        moves=M2_OFFSET_TENSION_MIRROR,
        player_to_move=1,
        description="Mirrored offset tension position, Black to move.",
    ),
    OpeningPosition(
        name="O8_diagonal_balance_mirror_white",
        moves=mirror_columns(swap_players(M3_DIAGONAL_BALANCE)),
        player_to_move=-1,
        description="Mirrored diagonal balance position, White to move.",
    ),
    OpeningPosition(
        name="O9_central_cross_variant_black",
        moves=M1_CENTRAL_CROSS_VARIANT,
        player_to_move=1,
        description="Expanded central-cross family, Black to move.",
    ),
    OpeningPosition(
        name="O10_diagonal_balance_white",
        moves=swap_players(M3_DIAGONAL_BALANCE),
        player_to_move=-1,
        description="Diagonal-balance family, White to move.",
    ),
]