from typing import List, Optional

from game.board import Board
from game.rules import find_winning_line, get_winner
from game.utils import print_board
from models import GameResult


def average(values: List[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def winner_to_text(winner: Optional[int]) -> str:
    if winner == 1:
        return "Black"
    if winner == -1:
        return "White"
    return "Draw"


def depth_winner_text(result: GameResult) -> str:
    """Return winner by depth, not by color."""
    if result.winner == 1:
        return f"Depth {result.black_depth} ({result.black_eval_name})"
    if result.winner == -1:
        return f"Depth {result.white_depth} ({result.white_eval_name})"
    return "Draw"


def print_final_result(
    board: Board,
    player1: int,
    player2: int,
    name1: str,
    name2: str,
    move_count: Optional[int] = None,
    total_time: Optional[float] = None,
) -> None:
    """
    Print final board state after a game.
    If there is a winner, highlight the winning line.
    """
    winner = get_winner(board)
    winning_line = find_winning_line(board)

    print("\n========== Final Board ==========")
    print_board(board, highlight=winning_line)

    print("\n========== Game Result ==========")

    if winner == player1:
        print(f"Winner: {name1}")
    elif winner == player2:
        print(f"Winner: {name2}")
    else:
        print("Result: Draw")

    if move_count is not None:
        print(f"Total moves: {move_count}")

    if total_time is not None:
        print(f"Total time: {total_time:.4f}s")

    print("=================================\n")


def print_game_result(result: GameResult, game_index: int, total_games: int) -> None:
    """Print one benchmark game result."""
    print("\n----------------------------------------")
    print(f"Game {game_index}/{total_games}")
    print(f"Black: depth {result.black_depth}, {result.black_eval_name}")
    print(f"White: depth {result.white_depth}, {result.white_eval_name}")
    print(f"Winner color: {winner_to_text(result.winner)}")
    print(f"Winner depth: {depth_winner_text(result)}")
    print(f"Moves: {result.moves}")
    print(f"Total time: {result.total_time:.4f}s")

    print(
        f"Black depth {result.black_depth} | "
        f"avg time/move={result.black_avg_time:.4f}s | "
        f"avg nodes/move={result.black_avg_nodes:.1f} | "
        f"avg prunes/move={result.black_avg_prunes:.1f}"
    )

    print(
        f"White depth {result.white_depth} | "
        f"avg time/move={result.white_avg_time:.4f}s | "
        f"avg nodes/move={result.white_avg_nodes:.1f} | "
        f"avg prunes/move={result.white_avg_prunes:.1f}"
    )
