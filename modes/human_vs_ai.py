from ai.player import ai_move
from cli.input import ask_ai_difficulty, parse_move
from cli.output import print_final_result
from game.board import Board
from game.rules import is_terminal
from game.utils import print_board


def play_human_vs_ai() -> None:
    """Human vs AI mode."""
    board = Board(15)

    HUMAN = 1
    AI = -1

    current = HUMAN

    difficulty_name, depth, eval_fn, eval_name, search_name = ask_ai_difficulty()

    print("\nHuman vs AI started.")
    print(f"AI difficulty = {difficulty_name}")
    print(f"AI search = {search_name}")
    print(f"AI depth = {depth}")
    print(f"AI evaluation = {eval_name}")
    print("Input: row col, for example: 7 7 or 7,7")
    print("Commands: u = undo, q = quit\n")

    print_board(board)

    while True:
        if current == HUMAN:
            s = input("\nYour move: ")
            mv = parse_move(s)

            if mv is None:
                if s.strip().lower() in ("q", "quit", "exit"):
                    print("Game exited.")
                    return

                print("Invalid input. Example: 7 7 or 7,7")
                continue

            if mv == ("UNDO", "UNDO"):
                if board.undo() is None:
                    print("No move to undo.")
                    continue

                board.undo()
                print_board(board)
                current = HUMAN
                continue

            r, c = mv

            if not board.place(r, c, HUMAN):
                print("Invalid move. Out of bounds or occupied.")
                continue

            if is_terminal(board):
                print_final_result(board, HUMAN, AI, "You", "AI")
                return

            print_board(board)
            current = AI

        else:
            r, c = ai_move(
                board=board,
                player=AI,
                depth=depth,
                eval_fn=eval_fn,
                eval_name=eval_name,
                search_name=search_name,
            )

            board.place(r, c, AI)

            print(f"\nAI plays: {r} {c}")

            if is_terminal(board):
                print_final_result(board, HUMAN, AI, "You", "AI")
                return

            print_board(board)
            current = HUMAN
