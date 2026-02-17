import argparse
import random
from typing import Optional, Tuple

from game.board import Board
from game.rules import is_terminal, get_winner, generate_candidate_moves
from game.utils import print_board

Move = Tuple[int, int]


def parse_move(s: str) -> Optional[Tuple[int, int] | tuple[str, str]]:
    """解析用户输入的走法"""
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


def ai_move_placeholder(board: Board) -> Move:
    """基础AI走法（随机选择）"""
    moves = generate_candidate_moves(board, radius=1)
    return random.choice(moves)


def play_human_vs_ai() -> None:
    """人机对战模式"""
    board = Board(15)
    HUMAN = 1
    AI = -1
    current = HUMAN

    print("五子棋开始！输入: 行 列 (例如: 7 7 或 7,7) | u=悔棋 | q=退出\n")
    print_board(board)

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
                print_board(board)
                current = HUMAN
                continue

            r, c = mv
            if not board.place(r, c, HUMAN):
                print("这里不能下（越界或已有棋子）。")
                continue

            print_board(board)
            if is_terminal(board):
                winner = get_winner(board)
                if winner == HUMAN:
                    print("\n你赢了！🎉")
                else:
                    print("\nAI 赢了。🤖")
                return

            current = AI

        else:
            r, c = ai_move_placeholder(board)
            board.place(r, c, AI)
            print(f"\nAI 下：{r} {c}")
            print_board(board)

            if is_terminal(board):
                winner = get_winner(board)
                if winner == AI:
                    print("\nAI 赢了。🤖")
                else:
                    print("\n你赢了！🎉")
                return

            current = HUMAN


def play_ai_vs_ai() -> None:
    """AI对战模式"""
    board = Board(15)
    AI1 = 1
    AI2 = -1
    current = AI1

    print("AI对战模式开始！\n")
    print_board(board)

    while True:
        r, c = ai_move_placeholder(board)
        board.place(r, c, current)
        print(f"\nAI{1 if current == AI1 else 2} 下：{r} {c}")
        print_board(board)

        if is_terminal(board):
            winner = get_winner(board)
            if winner:
                print(f"\nAI{1 if winner == AI1 else 2} 赢了！")
            else:
                print("\n平局！")
            return

        current = AI2 if current == AI1 else AI1


def run_tournament() -> None:
    """运行锦标赛模式"""
    print("锦标赛模式（待实现）")
    # 这里可以集成更复杂的AI算法进行比较


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="五子棋游戏")
    parser.add_argument("--mode", choices=["play", "tournament"], 
                       default="play", help="游戏模式")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    if args.mode == "play":
        play_human_vs_ai()
    elif args.mode == "tournament":
        run_tournament()
