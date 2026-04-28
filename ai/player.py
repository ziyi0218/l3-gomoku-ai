import random
import time
from typing import Tuple

from ai.minmax import choose_move_minimax
from game.board import Board
from game.rules import generate_candidate_moves
from models import EvalFn, Move, MoveStats


def ai_move_random(board: Board) -> Move:
    """Random fallback AI."""
    moves = generate_candidate_moves(board, radius=2)
    return random.choice(moves)


def ai_move_minimax_with_stats(
    board: Board,
    player: int,
    depth: int,
    eval_fn: EvalFn,
) -> Tuple[Move, MoveStats]:
    """Choose one move with Minimax and measure time + nodes."""
    start = time.perf_counter()

    move, stats = choose_move_minimax(
        board=board,
        player=player,
        depth=depth,
        eval_fn=eval_fn,
    )

    elapsed = time.perf_counter() - start

    if move is None:
        move = ai_move_random(board)

    return move, MoveStats(
        time_seconds=elapsed,
        nodes=stats.nodes_evaluated,
    )


def ai_move_minimax(
    board: Board,
    player: int,
    depth: int,
    eval_fn: EvalFn,
    eval_name: str,
) -> Move:
    """Visible AI move for normal play mode."""
    move, stats = ai_move_minimax_with_stats(
        board=board,
        player=player,
        depth=depth,
        eval_fn=eval_fn,
    )

    print(
        f"AI stats | depth={depth} | eval={eval_name} | "
        f"time={stats.time_seconds:.4f}s | "
        f"nodes={stats.nodes}"
    )

    return move
