from typing import List, Tuple
from game.board import Board

Move = Tuple[int, int]

EMPTY = 0
WIN_SCORE = 1_000_000

DIRECTIONS = [
    (1, 0),     # vertical
    (0, 1),     # horizontal
    (1, 1),     # diagonal down-right
    (1, -1),    # diagonal down-left
]


# ============================================================
# Basic helpers
# ============================================================

def in_bounds(board: Board, r: int, c: int) -> bool:
    return 0 <= r < board.size and 0 <= c < board.size


def opponent(player: int) -> int:
    return -player


def has_five(board: Board, player: int) -> bool:
    """
    Check whether player has five or more stones in a row.
    """
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


def terminal_score(board: Board, player: int) -> float | None:
    """
    Terminal score from player's perspective.
    """
    if has_five(board, player):
        return float(WIN_SCORE)

    if has_five(board, opponent(player)):
        return float(-WIN_SCORE)

    return None


# ============================================================
# Eval A: consecutive segment length
# ============================================================

def collect_segments(board: Board, player: int) -> List[int]:
    """
    Collect maximal consecutive segments.

    Example:
        XXX -> length 3
    """
    segments: List[int] = []

    for r, c in board.stones:
        if board.get(r, c) != player:
            continue

        for dr, dc in DIRECTIONS:
            prev_r = r - dr
            prev_c = c - dc

            # Only count from the start of a segment
            if in_bounds(board, prev_r, prev_c) and board.get(prev_r, prev_c) == player:
                continue

            length = 0
            nr, nc = r, c

            while in_bounds(board, nr, nc) and board.get(nr, nc) == player:
                length += 1
                nr += dr
                nc += dc

            if length > 0:
                segments.append(length)

    return segments


def score_segments_basic(segments: List[int]) -> float:
    """
    Eval A scoring:
    only cares about consecutive length.
    """
    weights = {
        1: 1,
        2: 10,
        3: 100,
        4: 10_000,
    }

    score = 0.0

    for length in segments:
        if length >= 5:
            score += WIN_SCORE
        else:
            score += weights.get(length, 0)

    return score


def eval_basic(board: Board, player: int) -> float:
    """
    Eval A:
    Basic defensive evaluation.

    Focus:
        优先防守对手的活二、活三、活四
    """
    terminal = terminal_score(board, player)
    if terminal is not None:
        return terminal

    my_segments = collect_segments(board, player)
    opp_segments = collect_segments(board, opponent(player))
    my_open_segments = collect_open_segments(board, player)
    opp_open_segments = collect_open_segments(board, opponent(player))

    my_score = score_segments_basic(my_segments)
    opp_score = score_segments_basic(opp_segments)

    return (
        my_score
        + score_open_segments_defensive(my_open_segments, is_opponent=False)
        - opp_score
        - score_open_segments_defensive(opp_open_segments, is_opponent=True)
    )


# ============================================================
# Eval B: consecutive segment length + open ends
# ============================================================

def collect_open_segments(board: Board, player: int) -> List[Tuple[int, int]]:
    """
    Collect maximal segments with open-end information.

    Return:
        [(length, open_ends), ...]

    open_ends:
        0 = both ends blocked
        1 = one end open
        2 = both ends open
    """
    segments: List[Tuple[int, int]] = []

    for r, c in board.stones:
        if board.get(r, c) != player:
            continue

        for dr, dc in DIRECTIONS:
            prev_r = r - dr
            prev_c = c - dc

            # Only count from the start of a segment
            if in_bounds(board, prev_r, prev_c) and board.get(prev_r, prev_c) == player:
                continue

            length = 0
            nr, nc = r, c

            while in_bounds(board, nr, nc) and board.get(nr, nc) == player:
                length += 1
                nr += dr
                nc += dc

            open_ends = 0

            # Cell before the segment
            if in_bounds(board, prev_r, prev_c) and board.get(prev_r, prev_c) == EMPTY:
                open_ends += 1

            # Cell after the segment
            if in_bounds(board, nr, nc) and board.get(nr, nc) == EMPTY:
                open_ends += 1

            segments.append((length, open_ends))

    return segments


def score_open_segments_defensive(
    segments: List[Tuple[int, int]],
    is_opponent: bool,
) -> float:
    """
    Coarse open-segment scoring for Eval A.

    Eval A stays simpler than Eval B, but reacts much more strongly to the
    opponent's open threats so its behavior is more conservative.
    """
    score = 0.0

    for length, open_ends in segments:
        if length >= 5:
            score += WIN_SCORE

        elif length == 4:
            if open_ends == 2:
                score += 60_000 if is_opponent else 12_000
            elif open_ends == 1:
                score += 18_000 if is_opponent else 4_000

        elif length == 3:
            if open_ends == 2:
                score += 3_500 if is_opponent else 350
            elif open_ends == 1:
                score += 700 if is_opponent else 90

        elif length == 2:
            if open_ends == 2:
                score += 160 if is_opponent else 40
            elif open_ends == 1:
                score += 40 if is_opponent else 10

    return score


def score_open_segments(segments: List[Tuple[int, int]]) -> float:
    """
    Eval B scoring:
    length + open ends.

    Examples:
        _XXX_  -> open three
        OXXX_  -> blocked three
        _XXXX_ -> open four
    """
    score = 0.0

    for length, open_ends in segments:
        if length >= 5:
            score += WIN_SCORE

        elif length == 4:
            if open_ends == 2:
                score += 80_000
            elif open_ends == 1:
                score += 15_000

        elif length == 3:
            if open_ends == 2:
                score += 1_500
            elif open_ends == 1:
                score += 250

        elif length == 2:
            if open_ends == 2:
                score += 80
            elif open_ends == 1:
                score += 20

        elif length == 1:
            if open_ends == 2:
                score += 3
            elif open_ends == 1:
                score += 1

    return score


def score_open_segment_combinations(segments: List[Tuple[int, int]]) -> float:
    """
    Reward compound threats that basic open-segment scoring misses.

    This stays simpler than Eval C: it only counts combinations of already
    detected contiguous open segments and does not inspect all five-cell windows.
    """
    open_fours = 0
    blocked_fours = 0
    open_threes = 0
    blocked_threes = 0

    for length, open_ends in segments:
        if length == 4:
            if open_ends == 2:
                open_fours += 1
            elif open_ends == 1:
                blocked_fours += 1
        elif length == 3:
            if open_ends == 2:
                open_threes += 1
            elif open_ends == 1:
                blocked_threes += 1

    score = 0.0

    if open_threes >= 2:
        score += 6_000

    if open_threes >= 1 and blocked_fours >= 1:
        score += 12_000

    if open_threes >= 1 and open_fours >= 1:
        score += 18_000

    if blocked_fours >= 2:
        score += 8_000

    if open_threes >= 1 and blocked_threes >= 1:
        score += 1_200

    return score


def eval_intermediate(board: Board, player: int) -> float:
    """
    Eval B:
    Consecutive segment length + open ends.

    Focus:
        棋形是否活
    """
    terminal = terminal_score(board, player)
    if terminal is not None:
        return terminal

    my_segments = collect_open_segments(board, player)
    opp_segments = collect_open_segments(board, opponent(player))

    my_score = (
        score_open_segments(my_segments)
        + score_open_segment_combinations(my_segments)
    )
    opp_score = (
        score_open_segments(opp_segments)
        + score_open_segment_combinations(opp_segments)
    )

    return my_score - 1.08 * opp_score


# ============================================================
# Eval C: five-cell window potential
# ============================================================

def get_all_five_windows(board: Board) -> List[List[int]]:
    """
    Generate all length-5 windows in four directions.

    Example:
        [1, 1, 0, 0, 0]
    """
    windows: List[List[int]] = []

    for r in range(board.size):
        for c in range(board.size):
            for dr, dc in DIRECTIONS:
                end_r = r + 4 * dr
                end_c = c + 4 * dc

                if not in_bounds(board, end_r, end_c):
                    continue

                window = []

                for i in range(5):
                    nr = r + i * dr
                    nc = c + i * dc
                    window.append(board.get(nr, nc))

                windows.append(window)

    return windows


def score_window(window: List[int], player: int) -> float:
    """
    Score one length-5 window from player's perspective.

    If both players appear in the same window,
    this window cannot directly become five-in-a-row.
    """
    opp = opponent(player)

    my_count = window.count(player)
    opp_count = window.count(opp)
    empty_count = window.count(EMPTY)

    # Blocked window
    if my_count > 0 and opp_count > 0:
        return 0.0

    # My potential window
    if my_count > 0 and opp_count == 0:
        if my_count == 5:
            return WIN_SCORE
        if my_count == 4 and empty_count == 1:
            return 50_000
        if my_count == 3 and empty_count == 2:
            return 3_000
        if my_count == 2 and empty_count == 3:
            return 300
        if my_count == 1 and empty_count == 4:
            return 20

    # Opponent potential window
    if opp_count > 0 and my_count == 0:
        if opp_count == 5:
            return -WIN_SCORE
        if opp_count == 4 and empty_count == 1:
            return -70_000
        if opp_count == 3 and empty_count == 2:
            return -4_000
        if opp_count == 2 and empty_count == 3:
            return -350
        if opp_count == 1 and empty_count == 4:
            return -20

    return 0.0


def center_bonus(board: Board, player: int) -> float:
    """
    Small positional bonus.

    Center stones are slightly better, but this bonus should stay small.
    """
    center = board.size // 2
    score = 0.0

    for r, c in board.stones:
        if board.get(r, c) == player:
            distance = abs(r - center) + abs(c - center)
            score += max(0, center - distance) * 0.5

    return score


def eval_advanced(board: Board, player: int) -> float:
    """
    Eval C:
    Five-cell window potential.

    Focus:
        是否存在可以形成五连的空间
    """
    terminal = terminal_score(board, player)
    if terminal is not None:
        return terminal

    score = 0.0

    for window in get_all_five_windows(board):
        score += score_window(window, player)

    score += center_bonus(board, player)
    score -= center_bonus(board, opponent(player))

    return score


# ============================================================
# Selector
# ============================================================

EVALUATION_FUNCTIONS = {
    "basic": eval_basic,
    "intermediate": eval_intermediate,
    "advanced": eval_advanced,
}