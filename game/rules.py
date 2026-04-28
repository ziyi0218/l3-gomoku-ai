from typing import Optional, Tuple, List
from game.board import Board

Move = Tuple[int, int]

DIRECTIONS = [
    (1, 0),     # vertical
    (0, 1),     # horizontal
    (1, 1),     # diagonal down-right
    (1, -1),    # diagonal down-left
]


def in_bounds(board: Board, r: int, c: int) -> bool:
    """
    Check whether a position is inside the board.
    """
    return 0 <= r < board.size and 0 <= c < board.size


def check_win_at(board: Board, r: int, c: int) -> bool:
    """
    Check whether the stone at (r, c) forms five in a row.
    """
    player = board.get(r, c)

    if player == 0:
        return False

    for dr, dc in DIRECTIONS:
        count = 1

        # Forward direction
        nr, nc = r + dr, c + dc
        while in_bounds(board, nr, nc) and board.get(nr, nc) == player:
            count += 1
            nr += dr
            nc += dc

        # Backward direction
        nr, nc = r - dr, c - dc
        while in_bounds(board, nr, nc) and board.get(nr, nc) == player:
            count += 1
            nr -= dr
            nc -= dc

        if count >= 5:
            return True

    return False


def find_winning_line(board: Board) -> Optional[List[Move]]:
    """
    Return the winning line if there is one.

    Return:
        List of 5 positions if a player has five in a row.
        None if there is no winner.
    """
    for r, c in board.stones:
        player = board.get(r, c)

        if player == 0:
            continue

        for dr, dc in DIRECTIONS:
            line: List[Move] = [(r, c)]

            # Forward direction
            nr, nc = r + dr, c + dc
            while in_bounds(board, nr, nc) and board.get(nr, nc) == player:
                line.append((nr, nc))
                nr += dr
                nc += dc

            # Backward direction
            nr, nc = r - dr, c - dc
            while in_bounds(board, nr, nc) and board.get(nr, nc) == player:
                line.insert(0, (nr, nc))
                nr -= dr
                nc -= dc

            if len(line) >= 5:
                return line[:5]

    return None


def get_winner(board: Board) -> Optional[int]:
    """
    Return the winner.

    Return:
        1    if black wins
        -1   if white wins
        None if no player wins
    """
    winning_line = find_winning_line(board)

    if winning_line is None:
        return None

    r, c = winning_line[0]
    return board.get(r, c)


def is_full(board: Board) -> bool:
    """
    Return True if the board is full.
    """
    return len(board.stones) >= board.size * board.size


def is_terminal(board: Board) -> bool:
    """
    Return True if the game is over.

    The game is over if:
    1. A player has five in a row.
    2. The board is full.
    """
    return get_winner(board) is not None or is_full(board)


def generate_legal_moves(board: Board) -> List[Move]:
    """
    Generate all legal moves on the board.
    """
    moves: List[Move] = []

    for r in range(board.size):
        for c in range(board.size):
            if board.is_empty(r, c):
                moves.append((r, c))

    return moves


def generate_candidate_moves(board: Board, radius: int = 2) -> List[Move]:
    """
    Generate candidate moves around existing stones.

    This is used to reduce the branching factor for Minimax / Alpha-Beta.

    If the board is empty, return the center position.
    Otherwise, return all empty cells within the given radius of existing stones.
    """
    if len(board.stones) == 0:
        center = board.size // 2
        return [(center, center)]

    candidates = set()

    for r, c in board.stones:
        for dr in range(-radius, radius + 1):
            for dc in range(-radius, radius + 1):
                nr = r + dr
                nc = c + dc

                if in_bounds(board, nr, nc) and board.is_empty(nr, nc):
                    candidates.add((nr, nc))

    return list(candidates)