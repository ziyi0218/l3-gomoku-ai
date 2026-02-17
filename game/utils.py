from game.board import Board


def format_board(board: Board) -> str:
    """格式化棋盘字符串"""
    # 每格宽度
    cell_w = 3

    # 列号
    header = " " * (cell_w) + "".join(f"{c:>{cell_w}}" for c in range(board.size))
    rows = [header]

    # 行内容
    for r in range(board.size):
        line = [f"{r:>{cell_w - 1}} "]  # 行号
        for c in range(board.size):
            v = board.grid[r][c]
            ch = "·" if v == 0 else ("X" if v == 1 else "O")
            line.append(f"{ch:>{cell_w}}")
        rows.append("".join(line))

    return "\n".join(rows)


def print_board(board: Board) -> None:
    """打印棋盘"""
    print(format_board(board))
