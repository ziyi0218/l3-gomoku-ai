from dataclasses import dataclass
from typing import List, Tuple, Optional, Set, Iterable

Move = Tuple[int, int]


@dataclass
class Board:
    """棋盘状态表示类"""
    size: int = 15

    def __post_init__(self) -> None:
        # 0 = 空, 1 = 黑, -1 = 白
        self.grid: List[List[int]] = [
            [0] * self.size for _ in range(self.size)
        ]
        self.move_stack: List[Tuple[int, int, int]] = []  # (r, c, player)
        self.stones: Set[Move] = set()

    # =========================
    # 基础工具
    # =========================
    def in_bounds(self, r: int, c: int) -> bool:
        """检查坐标是否在棋盘范围内"""
        return 0 <= r < self.size and 0 <= c < self.size

    def get(self, r: int, c: int) -> int:
        """获取指定位置的状态"""
        if not self.in_bounds(r, c):
            raise IndexError("Out of bounds")
        return self.grid[r][c]

    def is_empty(self, r: int, c: int) -> bool:
        """检查位置是否为空"""
        return self.in_bounds(r, c) and self.grid[r][c] == 0

    # =========================
    # 落子 / 悔棋
    # =========================
    def place(self, r: int, c: int, player: int) -> bool:
        """
        落子操作
        player: 1 (黑) / -1 (白)
        成功返回 True，否则 False
        """
        if player not in (1, -1):
            raise ValueError("player must be 1 or -1")

        if not self.is_empty(r, c):
            return False

        self.grid[r][c] = player
        self.move_stack.append((r, c, player))
        self.stones.add((r, c))
        return True

    def undo(self) -> Optional[Tuple[int, int, int]]:
        """撤销最后一步"""
        if not self.move_stack:
            return None

        r, c, player = self.move_stack.pop()
        self.grid[r][c] = 0
        self.stones.remove((r, c))
        return (r, c, player)

    def last_move(self) -> Optional[Tuple[int, int, int]]:
        """获取最后一步落子"""
        if not self.move_stack:
            return None
        return self.move_stack[-1]

    # =========================
    # 给 evaluation / win-check 用
    # =========================
    def iter_lines_through(self, r: int, c: int) -> Iterable[List[int]]:
        """
        返回经过 (r,c) 的4条方向线
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            line: List[int] = []

            rr, cc = r, c
            while self.in_bounds(rr - dr, cc - dc):
                rr -= dr
                cc -= dc

            while self.in_bounds(rr, cc):
                line.append(self.grid[rr][cc])
                rr += dr
                cc += dc

            yield line
