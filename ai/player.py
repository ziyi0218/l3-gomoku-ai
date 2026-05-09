import random
import time
from typing import Tuple

from ai.alphabeta import choose_move_alphabeta
from ai.minmax import choose_move_minimax
from game.board import Board
from game.rules import generate_candidate_moves
from models import EvalFn, Move, MoveStats

SEARCH_MINIMAX = "Minimax"
SEARCH_ALPHABETA = "Alpha-Beta"


def ai_move_random(board: Board) -> Move:
    """Random fallback AI."""
    moves = generate_candidate_moves(board, radius=2)
    return random.choice(moves)


def ai_move_with_stats(
    board: Board,
    player: int,
    depth: int,
    eval_fn: EvalFn,
    search_name: str = SEARCH_ALPHABETA,
    use_ordering: bool = True,
    candidate_radius: int = 2,
) -> Tuple[Move, MoveStats]:
    """Choose one move and measure time, nodes, and pruning."""
    start = time.perf_counter()

    if search_name == SEARCH_MINIMAX:
        move, _, stats = choose_move_minimax(
            board=board,
            player=player,
            depth=depth,
            eval_fn=eval_fn,
        )
    else:
        move, _, stats = choose_move_alphabeta(
            board=board,
            player=player,
            depth=depth,
            eval_fn=eval_fn,
            use_ordering=use_ordering,
            candidate_radius=candidate_radius,
        )

    elapsed = time.perf_counter() - start

    if move is None:
        move = ai_move_random(board)

    return move, MoveStats(
        time_seconds=elapsed,
        nodes=stats.nodes_evaluated,
        pruning_count=getattr(stats, "pruning_count", 0),
    )


def ai_move(
    board: Board,
    player: int,
    depth: int,
    eval_fn: EvalFn,
    eval_name: str,
    search_name: str = SEARCH_ALPHABETA,
    use_ordering: bool = True,
    candidate_radius: int = 2,
) -> Move:
    """Visible AI move for normal play mode."""
    move, stats = ai_move_with_stats(
        board=board,
        player=player,
        depth=depth,
        eval_fn=eval_fn,
        search_name=search_name,
        use_ordering=use_ordering,
        candidate_radius=candidate_radius,
    )

    ordering_label = "on" if use_ordering else "off"
    print(
        f"AI stats | search={search_name} | depth={depth} | eval={eval_name} | "
        f"ordering={ordering_label} | radius={candidate_radius} | "
        f"time={stats.time_seconds:.4f}s | "
        f"nodes={stats.nodes} | "
        f"prunes={stats.pruning_count}"
    )

    return move


def ai_move_minimax_with_stats(
    board: Board,
    player: int,
    depth: int,
    eval_fn: EvalFn,
) -> Tuple[Move, MoveStats]:
    """Backward-compatible wrapper for pure Minimax."""
    return ai_move_with_stats(
        board=board,
        player=player,
        depth=depth,
        eval_fn=eval_fn,
        search_name=SEARCH_MINIMAX,
        use_ordering=False,
    )


def ai_move_minimax(
    board: Board,
    player: int,
    depth: int,
    eval_fn: EvalFn,
    eval_name: str,
) -> Move:
    """Backward-compatible wrapper for pure Minimax."""
    return ai_move(
        board=board,
        player=player,
        depth=depth,
        eval_fn=eval_fn,
        eval_name=eval_name,
        search_name=SEARCH_MINIMAX,
        use_ordering=False,
    )
