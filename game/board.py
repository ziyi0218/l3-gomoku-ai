from dataclasses import dataclass
from typing import List, Tuple, Optional, Set, Iterable

Move = Tuple[int, int]


@dataclass
class Board:
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
        return 0 <= r < self.size and 0 <= c < self.size

    def get(self, r: int, c: int) -> int:
        if not self.in_bounds(r, c):
            raise IndexError("Out of bounds")
        return self.grid[r][c]

    def is_empty(self, r: int, c: int) -> bool:
        return self.in_bounds(r, c) and self.grid[r][c] == 0

    # =========================
    # 落子 / 悔棋
    # =========================
    def place(self, r: int, c: int, player: int) -> bool:
        """
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
        """
        撤销最后一步
        """
        if not self.move_stack:
            return None

        r, c, player = self.move_stack.pop()
        self.grid[r][c] = 0
        self.stones.remove((r, c))
        return (r, c, player)

    def last_move(self) -> Optional[Tuple[int, int, int]]:
        if not self.move_stack:
            return None
        return self.move_stack[-1]

    # =========================
    # 合法走法
    # =========================
    def get_valid_moves(self) -> List[Move]:
        """
        返回所有空位置（全盘搜索用，不推荐AI直接用）
        """
        moves: List[Move] = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    moves.append((r, c))
        return moves

    def get_candidate_moves(self, radius: int = 2) -> List[Move]:
        """
        AI推荐用：
        只返回已有棋子附近 radius 范围内的空点
        """
        if not self.stones:
            mid = self.size // 2
            return [(mid, mid)]

        candidates: Set[Move] = set()

        for r0, c0 in self.stones:
            for dr in range(-radius, radius + 1):
                for dc in range(-radius, radius + 1):
                    r, c = r0 + dr, c0 + dc
                    if self.is_empty(r, c):
                        candidates.add((r, c))

        # 按离中心距离排序（提高剪枝效率）
        mid = (self.size - 1) / 2
        return sorted(
            candidates,
            key=lambda mv: (mv[0] - mid) ** 2 + (mv[1] - mid) ** 2
        )

    # =========================
    # 打印棋盘（调试用）
    # =========================
    def __str__(self) -> str:
        # 每格宽度（3更舒服）
        cell_w = 3

        # 列号
        header = " " * (cell_w) + "".join(f"{c:>{cell_w}}" for c in range(self.size))
        rows = [header]

        # 行内容
        for r in range(self.size):
            line = [f"{r:>{cell_w - 1}} "]  # 行号
            for c in range(self.size):
                v = self.grid[r][c]
                ch = "·" if v == 0 else ("X" if v == 1 else "O")
                line.append(f"{ch:>{cell_w}}")
            rows.append("".join(line))

        return "\n".join(rows)

    def print(self) -> None:
        print(self)

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
