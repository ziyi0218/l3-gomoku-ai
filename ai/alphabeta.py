from typing import Tuple, Optional
from game.board import Board
from game.rules import is_terminal, generate_candidate_moves
from ai.evaluation import eval_basic

Move = Tuple[int, int]


class AlphaBetaStats:
    """Alpha-Beta算法统计信息"""
    def __init__(self):
        self.nodes_evaluated = 0
        self.pruning_count = 0
        self.max_depth_reached = 0


def alphabeta(board: Board, depth: int, alpha: float, beta: float,
              maximizing_player: bool, stats: AlphaBetaStats) -> Tuple[float, Optional[Move]]:
    """
    Alpha-Beta剪枝算法
    """
    stats.nodes_evaluated += 1
    stats.max_depth_reached = max(stats.max_depth_reached, depth)
    
    if depth == 0 or is_terminal(board):
        return eval_basic(board, 1 if maximizing_player else -1), None
    
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        
        for move in generate_candidate_moves(board):
            # 模拟落子
            if board.place(move[0], move[1], 1):
                eval_score, _ = alphabeta(board, depth - 1, alpha, beta, False, stats)
                board.undo()  # 撤销
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    stats.pruning_count += 1
                    break  # Beta剪枝
        
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        
        for move in generate_candidate_moves(board):
            # 模拟落子
            if board.place(move[0], move[1], -1):
                eval_score, _ = alphabeta(board, depth - 1, alpha, beta, True, stats)
                board.undo()  # 撤销
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    stats.pruning_count += 1
                    break  # Alpha剪枝
        
        return min_eval, best_move
