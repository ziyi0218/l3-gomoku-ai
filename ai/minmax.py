from typing import Tuple, Optional, Callable

from game.board import Board
from game.rules import is_terminal, generate_candidate_moves
from ai.evaluation import eval_basic

Move = Tuple[int, int]
EvalFn = Callable[[Board, int], float]


class MinimaxStats:
    """Minimax算法统计信息"""

    def __init__(self):
        self.nodes_evaluated = 0
        self.max_depth_reached = 0


def choose_move_minimax(
    board: Board,
    player: int,
    depth: int,
    eval_fn: EvalFn = eval_basic,
) -> Tuple[Optional[Move], MinimaxStats]:
    """
    对外接口：main.py 调用这个函数来选择一步棋。
    """
    stats = MinimaxStats()

    _, best_move = minimax(
        board=board,
        depth=depth,
        current_player=player,
        root_player=player,
        eval_fn=eval_fn,
        stats=stats,
        current_depth=0,
    )

    return best_move, stats


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
    纯 Minimax 算法。

    current_player: 当前轮到谁下
    root_player: 最初调用搜索的 AI 玩家

    evaluation 永远从 root_player 的角度打分。
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

    else:
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