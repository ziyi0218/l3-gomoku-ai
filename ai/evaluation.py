import random
from typing import Tuple
from game.board import Board
from game.rules import generate_candidate_moves

Move = Tuple[int, int]


def eval_basic(board: Board, player: int) -> float:
    """基础评估函数 - 随机选择"""
    return random.uniform(-1, 1)


def eval_intermediate(board: Board, player: int) -> float:
    """中级评估函数 - 基于棋子位置和连子数"""
    score = 0.0
    
    # 简单的评估逻辑（待完善）
    for r, c in board.stones:
        if board.get(r, c) == player:
            score += 1.0
        else:
            score -= 1.0
    
    return score


def eval_advanced(board: Board, player: int) -> float:
    """高级评估函数 - 考虑棋型和威胁"""
    # 更复杂的评估逻辑（待实现）
    return eval_intermediate(board, player)


def ai_move_basic(board: Board) -> Move:
    """基础AI走法（随机选择候选点）"""
    moves = generate_candidate_moves(board, radius=2)
    return random.choice(moves)
