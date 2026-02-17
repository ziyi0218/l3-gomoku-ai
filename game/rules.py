from typing import List, Optional, Tuple, Set
from game.board import Board

Move = Tuple[int, int]


def is_terminal(board: Board) -> bool:
    """判断游戏是否结束"""
    # 检查最后一步是否导致胜利
    last_move = board.last_move()
    if last_move:
        r, c, player = last_move
        if check_win_at(board, r, c):
            return True
    
    # 检查棋盘是否已满
    return len(board.stones) == board.size * board.size


def get_winner(board: Board) -> Optional[int]:
    """获取胜利者"""
    last_move = board.last_move()
    if last_move:
        r, c, player = last_move
        if check_win_at(board, r, c):
            return player
    return None


def check_win_at(board: Board, r: int, c: int) -> bool:
    """检查指定位置是否形成五连"""
    player = board.get(r, c)
    if player == 0:
        return False

    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in dirs:
        count = 1

        # 正向检查
        rr, cc = r + dr, c + dc
        while board.in_bounds(rr, cc) and board.get(rr, cc) == player:
            count += 1
            rr += dr
            cc += dc

        # 反向检查
        rr, cc = r - dr, c - dc
        while board.in_bounds(rr, cc) and board.get(rr, cc) == player:
            count += 1
            rr -= dr
            cc -= dc

        if count >= 5:
            return True

    return False


def generate_legal_moves(board: Board) -> List[Move]:
    """生成所有合法走法"""
    moves: List[Move] = []
    for r in range(board.size):
        for c in range(board.size):
            if board.grid[r][c] == 0:
                moves.append((r, c))
    return moves


def generate_candidate_moves(board: Board, radius: int = 2) -> List[Move]:
    """
    AI推荐用：只返回已有棋子附近 radius 范围内的空点
    """
    if not board.stones:
        mid = board.size // 2
        return [(mid, mid)]

    candidates: Set[Move] = set()

    for r0, c0 in board.stones:
        for dr in range(-radius, radius + 1):
            for dc in range(-radius, radius + 1):
                r, c = r0 + dr, c0 + dc
                if board.is_empty(r, c):
                    candidates.add((r, c))

    # 按离中心距离排序（提高剪枝效率）
    mid = (board.size - 1) / 2
    return sorted(
        candidates,
        key=lambda mv: (mv[0] - mid) ** 2 + (mv[1] - mid) ** 2
    )
