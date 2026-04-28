import time
from typing import Callable, List, Optional, Tuple

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
        self.candidate_count = 0
        self.time_ms = 0.0

    @property
    def nodes(self) -> int:
        return self.nodes_evaluated

    @property
    def cutoffs(self) -> int:
        return self.pruning_count

    @property
    def depth(self) -> int:
        return self.max_depth_reached


def choose_move_alphabeta(
    board: Board,
    player: int,
    depth: int,
    eval_fn: EvalFn = eval_basic,
    use_ordering: bool = False,
) -> Tuple[Optional[Move], float, AlphaBetaStats]:
    """Choose one move with Alpha-Beta pruning."""
    stats = AlphaBetaStats()
    stats.candidate_count = len(generate_candidate_moves(board, radius=2))

    start = time.perf_counter()
    score, best_move = alphabeta(
        board=board,
        depth=depth,
        alpha=float("-inf"),
        beta=float("inf"),
        current_player=player,
        root_player=player,
        eval_fn=eval_fn,
        stats=stats,
        current_depth=0,
        use_ordering=use_ordering,
    )
    stats.time_ms = (time.perf_counter() - start) * 1000

    return best_move, score, stats


def ordered_moves(
    board: Board,
    moves: List[Move],
    current_player: int,
    root_player: int,
    eval_fn: EvalFn,
) -> List[Move]:
    """
    Order candidates with a shallow static evaluation.

    The candidate set is unchanged; only traversal order changes. Maximizing
    layers inspect high-scoring moves first, minimizing layers low-scoring moves
    first, which generally helps Alpha-Beta prune earlier.
    """
    maximizing = current_player == root_player
    scored_moves = []

    for index, (r, c) in enumerate(moves):
        if board.place(r, c, current_player):
            score = eval_fn(board, root_player)
            board.undo()
            scored_moves.append((score, index, (r, c)))

    if maximizing:
        scored_moves.sort(key=lambda item: (-item[0], item[1]))
    else:
        scored_moves.sort(key=lambda item: (item[0], item[1]))

    return [move for _, _, move in scored_moves]


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
    use_ordering: bool,
) -> Tuple[float, Optional[Move]]:
    """
    Alpha-Beta pruning version of Minimax.

    Evaluation is always computed from root_player's point of view.
    """
    stats.nodes_evaluated += 1
    stats.max_depth_reached = max(stats.max_depth_reached, current_depth)

    if depth == 0 or is_terminal(board):
        return eval_fn(board, root_player), None

    moves = generate_candidate_moves(board, radius=2)

    if not moves:
        return eval_fn(board, root_player), None

    if use_ordering:
        moves = ordered_moves(board, moves, current_player, root_player, eval_fn)

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
                    use_ordering=use_ordering,
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
                use_ordering=use_ordering,
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
