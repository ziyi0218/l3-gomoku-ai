from typing import Callable, Optional, Tuple

from ai.evaluation import eval_basic
from game.board import Board
from game.rules import generate_candidate_moves, is_terminal

Move = Tuple[int, int]
EvalFn = Callable[[Board, int], float]


class AlphaBetaStats:
    """Alpha-Beta search statistics."""

    def __init__(self):
        self.nodes_evaluated = 0
        self.pruning_count = 0
        self.max_depth_reached = 0


def choose_move_alphabeta(
    board: Board,
    player: int,
    depth: int,
    eval_fn: EvalFn = eval_basic,
) -> Tuple[Optional[Move], AlphaBetaStats]:
    """Public interface for choosing one move with Alpha-Beta pruning."""
    stats = AlphaBetaStats()

    _, best_move = alphabeta(
        board=board,
        depth=depth,
        alpha=float("-inf"),
        beta=float("inf"),
        current_player=player,
        root_player=player,
        eval_fn=eval_fn,
        stats=stats,
        current_depth=0,
    )

    return best_move, stats


def alphabeta(
    board: Board,
    depth: int,
    alpha: float,
    beta: float,
    current_player: int,
    root_player: int,
    eval_fn: EvalFn,
    stats: AlphaBetaStats,
    current_depth: int,
) -> Tuple[float, Optional[Move]]:
    """
    Alpha-Beta pruning version of Minimax.

    It uses the same scoring perspective as Minimax: evaluation is always
    computed from root_player's point of view.
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
                score, _ = alphabeta(
                    board=board,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
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

                alpha = max(alpha, best_score)
                if beta <= alpha:
                    stats.pruning_count += 1
                    break

        return best_score, best_move

    best_score = float("inf")
    best_move = None

    for r, c in moves:
        if board.place(r, c, current_player):
            score, _ = alphabeta(
                board=board,
                depth=depth - 1,
                alpha=alpha,
                beta=beta,
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

            beta = min(beta, best_score)
            if beta <= alpha:
                stats.pruning_count += 1
                break

    return best_score, best_move
