from game.board import Board

WIN_SCORE = 1_000_000

DIRECTIONS = [
    (1, 0),
    (0, 1),
    (1, 1),
    (1, -1),
]


def in_bounds(board: Board, r: int, c: int) -> bool:
    return 0 <= r < board.size and 0 <= c < board.size


def has_five(board: Board, player: int) -> bool:
    for r, c in board.stones:
        if board.get(r, c) != player:
            continue

        for dr, dc in DIRECTIONS:
            count = 1

            nr, nc = r + dr, c + dc
            while in_bounds(board, nr, nc) and board.get(nr, nc) == player:
                count += 1
                nr += dr
                nc += dc

            nr, nc = r - dr, c - dc
            while in_bounds(board, nr, nc) and board.get(nr, nc) == player:
                count += 1
                nr -= dr
                nc -= dc

            if count >= 5:
                return True

    return False


def count_line(board: Board, r: int, c: int, dr: int, dc: int, player: int) -> int:
    count = 1

    nr, nc = r + dr, c + dc
    while in_bounds(board, nr, nc) and board.get(nr, nc) == player:
        count += 1
        nr += dr
        nc += dc

    nr, nc = r - dr, c - dc
    while in_bounds(board, nr, nc) and board.get(nr, nc) == player:
        count += 1
        nr -= dr
        nc -= dc

    return count


def pattern_score(board: Board, player: int) -> float:
    score = 0.0

    weights = {
        1: 1,
        2: 10,
        3: 100,
        4: 10_000,
    }

    for r, c in board.stones:
        if board.get(r, c) != player:
            continue

        for dr, dc in DIRECTIONS:
            length = count_line(board, r, c, dr, dc, player)

            if length >= 5:
                score += WIN_SCORE
            else:
                score += weights.get(length, 0)

    return score


def eval_basic(board: Board, player: int) -> float:
    """
    固定 evaluation，用来测试不同 depth。

    分数越高，说明局面对 player 越好。
    """
    if has_five(board, player):
        return float(WIN_SCORE)

    if has_five(board, -player):
        return float(-WIN_SCORE)

    return pattern_score(board, player) - pattern_score(board, -player)