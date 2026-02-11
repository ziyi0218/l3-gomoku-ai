import random
from typing import Optional, Tuple

from game.board import Board

Move = Tuple[int, int]


def parse_move(s: str) -> Optional[Tuple[int, int] | tuple[str, str]]:
    s = s.strip().lower()
    if s in ("q", "quit", "exit"):
        return None
    if s in ("u", "undo"):
        return ("UNDO", "UNDO")
    s = s.replace("，", ",").replace(" ", ",")
    parts = [p for p in s.split(",") if p]
    if len(parts) != 2:
        return None
    try:
        return (int(parts[0]), int(parts[1]))
    except ValueError:
        return None


def check_win(board: Board, r: int, c: int) -> bool:
    player = board.get(r, c)
    if player == 0:
        return False

    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in dirs:
        count = 1

        rr, cc = r + dr, c + dc
        while board.in_bounds(rr, cc) and board.get(rr, cc) == player:
            count += 1
            rr += dr
            cc += dc

        rr, cc = r - dr, c - dc
        while board.in_bounds(rr, cc) and board.get(rr, cc) == player:
            count += 1
            rr -= dr
            cc -= dc

        if count >= 5:
            return True

    return False


def ai_move_placeholder(board: Board) -> Move:
    moves = board.get_candidate_moves(radius=2)
    return random.choice(moves)


def play() -> None:
    board = Board(15)

    HUMAN = 1
    AI = -1
    current = HUMAN

    print("五子棋开始！输入: 行 列 (例如: 7 7 或 7,7) | u=悔棋 | q=退出\n")
    board.print()

    while True:
        if current == HUMAN:
            s = input("\n你下 (row col): ")
            mv = parse_move(s)

            if mv is None:
                if s.strip().lower() in ("q", "quit", "exit"):
                    print("已退出。")
                    return
                print("输入格式不对。例：7 7 或 7,7；命令：u 悔棋，q 退出")
                continue

            if mv == ("UNDO", "UNDO"):
                if board.undo() is None:
                    print("没棋可悔。")
                    continue
                board.undo()  # 人机对局通常悔两步
                board.print()
                current = HUMAN
                continue

            r, c = mv
            if not board.place(r, c, HUMAN):
                print("这里不能下（越界或已有棋子）。")
                continue

            board.print()
            if check_win(board, r, c):
                print("\n你赢了！🎉")
                return

            current = AI

        else:
            r, c = ai_move_placeholder(board)
            board.place(r, c, AI)
            print(f"\nAI 下：{r} {c}")
            board.print()

            if check_win(board, r, c):
                print("\nAI 赢了。🤖")
                return

            current = HUMAN


if __name__ == "__main__":
    play()

