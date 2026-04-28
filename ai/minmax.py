import time
from typing import Callable, Optional, Tuple

from ai.evaluation import eval_basic
from game.board import Board
from game.rules import generate_candidate_moves, is_terminal

Move = Tuple[int, int]
EvalFn = Callable[[Board, int], float]


class MinimaxStats:
    """Minimax search statistics."""

    def __init__(self):
        self.nodes_evaluated = 0
        self.max_depth_reached = 0
        self.cutoffs = 0
        self.candidate_count = 0
        self.time_ms = 0.0

    @property
    def nodes(self) -> int:
        return self.nodes_evaluated

    @property
    def depth(self) -> int:
        return self.max_depth_reached


def choose_move_minimax(
    board: Board,
    player: int,
    depth: int,
    eval_fn: EvalFn = eval_basic,
) -> Tuple[Optional[Move], float, MinimaxStats]:
    """Choose one move with pure Minimax."""
    stats = MinimaxStats()
    stats.candidate_count = len(generate_candidate_moves(board, radius=2))

    start = time.perf_counter()
    score, best_move = minimax(
        board=board,
        depth=depth,
        current_player=player,
        root_player=player,
        eval_fn=eval_fn,
        stats=stats,
        current_depth=0,
    )
    stats.time_ms = (time.perf_counter() - start) * 1000

    return best_move, score, stats


def minimax(
    board: Board,
    depth: int,
    current_player: int,
    root_player: int,
    eval_fn: EvalFn,
    stats: MinimaxStats,
    current_depth: int,
) -> Tuple[float, Optional[Move]]:
    """
    Pure Minimax.

    Evaluation is always computed from root_player's point of view.
    """
    stats.nodes_evaluated += 1
    stats.max_depth_reached = max(stats.max_depth_reached, current_depth)

    if depth == 0 or is_terminal(board):
        return eval_fn(board, root_player), None

    moves = generate_candidate_moves(board, radius=2)

    if not moves:
        return eval_fn(board, root_player), None

    maximizing = current_player == root_player

    if maximizing:
        best_score = float("-inf")
        best_move = None

        for r, c in moves:
            if board.place(r, c, current_player):
                score, _ = minimax(
                    board=board,
                    depth=depth - 1,
                    current_player=-current_player,
                    root_player=root_player,
                    eval_fn=eval_fn,
                    stats=stats,
                    current_depth=current_depth + 1,
                )
                board.undo()

                if score > best_score:
                    best_score = score
                    best_move = (r, c)

        return best_score, best_move

    best_score = float("inf")
    best_move = None

    for r, c in moves:
        if board.place(r, c, current_player):
            score, _ = minimax(
                board=board,
                depth=depth - 1,
                current_player=-current_player,
                root_player=root_player,
                eval_fn=eval_fn,
                stats=stats,
                current_depth=current_depth + 1,
            )
            board.undo()

            if score < best_score:
                best_score = score
                best_move = (r, c)

    return best_score, best_move
