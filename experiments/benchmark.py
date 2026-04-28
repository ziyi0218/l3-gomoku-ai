import time
from typing import List

from ai.player import ai_move_minimax_with_stats
from cli.output import average, print_final_result
from game.board import Board
from game.rules import get_winner, is_terminal
from game.utils import print_board
from models import EvalFn, GameResult


def run_one_benchmark_game(
    black_depth: int,
    white_depth: int,
    black_eval_fn: EvalFn,
    white_eval_fn: EvalFn,
    black_eval_name: str,
    white_eval_name: str,
    max_moves: int,
    print_final_board: bool,
    print_each_step: bool = False,
) -> GameResult:
    """
    Run one AI vs AI game for benchmark.

    Black always plays first.
    """
    board = Board(15)

    BLACK = 1
    WHITE = -1
    current = BLACK

    move_count = 0

    black_times: List[float] = []
    white_times: List[float] = []
    black_nodes: List[int] = []
    white_nodes: List[int] = []

    game_start = time.perf_counter()

    if print_each_step:
        print("\nInitial board:")
        print_board(board)

    while move_count < max_moves:
        if current == BLACK:
            depth = black_depth
            eval_fn = black_eval_fn
            eval_name = black_eval_name
            player_name = "Black"
        else:
            depth = white_depth
            eval_fn = white_eval_fn
            eval_name = white_eval_name
            player_name = "White"

        move, move_stats = ai_move_minimax_with_stats(
            board=board,
            player=current,
            depth=depth,
            eval_fn=eval_fn,
        )

        r, c = move
        board.place(r, c, current)
        move_count += 1

        if current == BLACK:
            black_times.append(move_stats.time_seconds)
            black_nodes.append(move_stats.nodes)
        else:
            white_times.append(move_stats.time_seconds)
            white_nodes.append(move_stats.nodes)

        if print_each_step:
            print("\n----------------------------------------")
            print(f"Move {move_count}")
            print(f"{player_name} plays: {r} {c}")
            print(f"Depth: {depth}")
            print(f"Evaluation: {eval_name}")
            print(f"Time: {move_stats.time_seconds:.4f}s")
            print(f"Nodes: {move_stats.nodes}")
            print_board(board)

        if is_terminal(board):
            break

        current = WHITE if current == BLACK else BLACK

    total_time = time.perf_counter() - game_start
    winner = get_winner(board)

    result = GameResult(
        winner=winner,
        moves=move_count,
        total_time=total_time,

        black_depth=black_depth,
        white_depth=white_depth,

        black_eval_name=black_eval_name,
        white_eval_name=white_eval_name,

        black_avg_time=average(black_times),
        white_avg_time=average(white_times),

        black_avg_nodes=average(black_nodes),
        white_avg_nodes=average(white_nodes),
    )

    if print_final_board:
        print_final_result(
            board=board,
            player1=BLACK,
            player2=WHITE,
            name1=f"Black depth {black_depth} ({black_eval_name})",
            name2=f"White depth {white_depth} ({white_eval_name})",
            move_count=move_count,
            total_time=total_time,
        )

    return result
