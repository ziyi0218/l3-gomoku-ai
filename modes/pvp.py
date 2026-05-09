from cli.input import parse_move
from cli.output import print_final_result
from game.board import Board
from game.rules import is_terminal
from game.utils import print_board


def play_pvp() -> None:
    """Two human players on the same terminal."""
    board = Board(15)

    BLACK = 1
    WHITE = -1
    current = BLACK
    move_count = 0

    print("\nPvP mode started.")
    print("Black = Player 1, White = Player 2")
    print("Input: row col, for example: 7 7 or 7,7")
    print("Commands: u = undo, q = quit\n")

    print_board(board)

    while True:
        player_name = "Player 1 (Black)" if current == BLACK else "Player 2 (White)"
        raw = input(f"\n{player_name} move: ")
        move = parse_move(raw)

        if move is None:
            if raw.strip().lower() in ("q", "quit", "exit"):
                print("Game exited.")
                return
            print("Invalid input. Example: 7 7 or 7,7")
            continue

        if move == ("UNDO", "UNDO"):
            undone = board.undo()
            if undone is None:
                print("No move to undo.")
                continue
            move_count -= 1
            current = undone[2]
            print_board(board)
            continue

        r, c = move
        if not board.place(r, c, current):
            print("Invalid move. Out of bounds or occupied.")
            continue

        move_count += 1

        if is_terminal(board):
            print_final_result(
                board=board,
                player1=BLACK,
                player2=WHITE,
                name1="Player 1",
                name2="Player 2",
                move_count=move_count,
            )
            return

        print_board(board)
        current = WHITE if current == BLACK else BLACK
