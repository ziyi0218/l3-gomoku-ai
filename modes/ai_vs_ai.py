from ai.player import ai_move
from cli.input import ask_ai_difficulty
from cli.output import print_final_result
from game.board import Board
from game.rules import is_terminal
from game.utils import print_board


def play_ai_vs_ai() -> None:
    """AI vs AI mode with fixed difficulty profiles."""
    board = Board(15)

    AI1 = 1
    AI2 = -1

    print("\nAI vs AI mode.")

    print("\nChoose difficulty for AI1:")
    difficulty_ai1, depth_ai1, eval_ai1, eval_name_ai1, search_ai1 = ask_ai_difficulty()

    print("\nChoose difficulty for AI2:")
    difficulty_ai2, depth_ai2, eval_ai2, eval_name_ai2, search_ai2 = ask_ai_difficulty()

    current = AI1
    move_count = 0

    print("\nAI vs AI started.\n")
    print(f"AI1 = Black, {difficulty_ai1}, {search_ai1}, depth {depth_ai1}, {eval_name_ai1}")
    print(f"AI2 = White, {difficulty_ai2}, {search_ai2}, depth {depth_ai2}, {eval_name_ai2}\n")

    print_board(board)

    while True:
        if current == AI1:
            depth = depth_ai1
            search_name = search_ai1
            eval_fn = eval_ai1
            eval_name = eval_name_ai1
            ai_name = "AI1"
        else:
            depth = depth_ai2
            search_name = search_ai2
            eval_fn = eval_ai2
            eval_name = eval_name_ai2
            ai_name = "AI2"

        r, c = ai_move(
            board=board,
            player=current,
            depth=depth,
            eval_fn=eval_fn,
            eval_name=eval_name,
            search_name=search_name,
        )

        board.place(r, c, current)
        move_count += 1

        print(f"\n{ai_name} plays: {r} {c}")

        if is_terminal(board):
            print_final_result(
                board=board,
                player1=AI1,
                player2=AI2,
                name1="AI1",
                name2="AI2",
                move_count=move_count,
            )
            return

        print_board(board)

        current = AI2 if current == AI1 else AI1
