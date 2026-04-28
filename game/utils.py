from typing import Optional, Iterable, Tuple
from game.board import Board

Move = Tuple[int, int]

RED = "\033[91m"
RESET = "\033[0m"


def format_board(board: Board, highlight: Optional[Iterable[Move]] = None) -> str:
    """
    Format board as string.
    If highlight is provided, those positions are shown in red.
    """
    highlight_set = set(highlight) if highlight else set()

    lines = []

    header = "    " + " ".join(f"{i:2}" for i in range(board.size))
    lines.append(header)

    for r in range(board.size):
        row = [f"{r:2} "]

        for c in range(board.size):
            value = board.get(r, c)

            if value == 1:
                symbol = "X"
            elif value == -1:
                symbol = "O"
            else:
                symbol = "."

            if (r, c) in highlight_set:
                symbol = f"{RED}{symbol}{RESET}"

            row.append(f"{symbol:>2}")

        lines.append(" ".join(row))

    return "\n".join(lines)


def print_board(board: Board, highlight: Optional[Iterable[Move]] = None) -> None:
    """
    Print board.
    Winning stones can be highlighted in red.
    """
    print(format_board(board, highlight))