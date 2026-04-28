import random
import time
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict

from game.board import Board
from game.rules import (
    is_terminal,
    get_winner,
    generate_candidate_moves,
    find_winning_line,
)
from game.utils import print_board

from ai.minmax import choose_move_minimax
from ai.evaluation import eval_basic

Move = Tuple[int, int]


# ============================================================
# Data classes
# ============================================================

@dataclass
class MoveStats:
    time_seconds: float
    nodes: int


@dataclass
class GameResult:
    winner: Optional[int]
    moves: int
    total_time: float

    black_depth: int
    white_depth: int

    black_avg_time: float
    white_avg_time: float

    black_avg_nodes: float
    white_avg_nodes: float


# ============================================================
# Input helpers
# ============================================================

def parse_move(s: str) -> Optional[Tuple[int, int] | tuple[str, str]]:
    """Parse human input."""
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
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None


def ask_int(prompt: str, valid_values: List[int]) -> int:
    """Ask user for an integer from valid values."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value in valid_values:
                return value
            print(f"Please choose one of: {valid_values}")
        except ValueError:
            print("Please enter a valid number.")


def ask_depth() -> int:
    """Ask user to choose one search depth."""
    print("\nChoose AI search depth / profondeur:")
    print("1. Depth 1")
    print("2. Depth 2")
    print("3. Depth 3")

    return ask_int("Your choice: ", [1, 2, 3])


def ask_depth_list() -> List[int]:
    """
    Ask user which depths to benchmark.

    Example:
        1 2
        1 2 3
    """
    while True:
        raw = input(
            "\nWhich depths do you want to test? "
            "Enter values like '1 2' or '1 2 3': "
        ).strip()

        parts = raw.replace(",", " ").split()

        try:
            depths = sorted(set(int(x) for x in parts))
        except ValueError:
            print("Please enter numbers only, for example: 1 2 3")
            continue

        if len(depths) < 2:
            print("Please choose at least two depths.")
            continue

        if any(d not in [1, 2, 3] for d in depths):
            print("Allowed depths are only 1, 2, and 3.")
            continue

        return depths


def ask_positive_int(prompt: str) -> int:
    """Ask user for any positive integer."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value > 0:
                return value
            print("Please enter a positive integer.")
        except ValueError:
            print("Please enter a valid number.")


# ============================================================
# Utility helpers
# ============================================================

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
    """
    Return winner by depth, not by color.
    """
    if result.winner == 1:
        return f"Depth {result.black_depth}"
    if result.winner == -1:
        return f"Depth {result.white_depth}"
    return "Draw"


# ============================================================
# AI helpers
# ============================================================

def ai_move_random(board: Board) -> Move:
    """Random fallback AI."""
    moves = generate_candidate_moves(board, radius=2)
    return random.choice(moves)


def ai_move_minimax_with_stats(
    board: Board,
    player: int,
    depth: int,
) -> Tuple[Move, MoveStats]:
    """
    Choose one move with Minimax and measure time + nodes.
    """
    start = time.perf_counter()

    move, stats = choose_move_minimax(
        board=board,
        player=player,
        depth=depth,
        eval_fn=eval_basic,
    )

    elapsed = time.perf_counter() - start

    if move is None:
        move = ai_move_random(board)

    return move, MoveStats(
        time_seconds=elapsed,
        nodes=stats.nodes_evaluated,
    )


def ai_move_minimax(board: Board, player: int, depth: int) -> Move:
    """
    Visible AI move for normal play mode.
    """
    move, stats = ai_move_minimax_with_stats(board, player, depth)

    print(
        f"AI stats | depth={depth} | "
        f"time={stats.time_seconds:.4f}s | "
        f"nodes={stats.nodes}"
    )

    return move


# ============================================================
# Result printing
# ============================================================

def print_final_result(
    board: Board,
    player1: int,
    player2: int,
    name1: str,
    name2: str,
    move_count: Optional[int] = None,
) -> None:
    """
    Print final board with highlighted winning line.
    """
    winner = get_winner(board)
    winning_line = find_winning_line(board)

    print_board(board, highlight=winning_line)

    if winner == player1:
        print(f"\n{name1} wins!")
    elif winner == player2:
        print(f"\n{name2} wins!")
    else:
        print("\nDraw!")

    if move_count is not None:
        print(f"Total moves: {move_count}")


# ============================================================
# Human vs AI
# ============================================================

def play_human_vs_ai() -> None:
    """Human vs AI mode."""
    board = Board(15)

    HUMAN = 1
    AI = -1

    current = HUMAN
    depth = ask_depth()

    print("\nHuman vs AI started.")
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
            r, c = ai_move_minimax(board, AI, depth)
            board.place(r, c, AI)

            print(f"\nAI plays: {r} {c}")

            if is_terminal(board):
                print_final_result(board, HUMAN, AI, "You", "AI")
                return

            print_board(board)
            current = HUMAN


# ============================================================
# AI vs AI normal mode
# ============================================================

def play_ai_vs_ai() -> None:
    """AI vs AI mode with depth selection."""
    board = Board(15)

    AI1 = 1
    AI2 = -1

    print("\nAI vs AI mode.")
    print("Choose depth for AI1:")
    depth_ai1 = ask_depth()

    print("\nChoose depth for AI2:")
    depth_ai2 = ask_depth()

    current = AI1
    move_count = 0

    print("\nAI vs AI started.\n")
    print(f"AI1 = Black, depth {depth_ai1}")
    print(f"AI2 = White, depth {depth_ai2}\n")

    print_board(board)

    while True:
        if current == AI1:
            depth = depth_ai1
            ai_name = "AI1"
        else:
            depth = depth_ai2
            ai_name = "AI2"

        r, c = ai_move_minimax(board, current, depth)

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


# ============================================================
# Benchmark game
# ============================================================

def play_ai_game_silent(
    black_depth: int,
    white_depth: int,
    max_moves: int,
) -> GameResult:
    """
    Run one AI vs AI game without printing the board.

    Black always plays first.
    The caller decides which depth is black and which depth is white.
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

    while move_count < max_moves:
        depth = black_depth if current == BLACK else white_depth

        move, move_stats = ai_move_minimax_with_stats(
            board=board,
            player=current,
            depth=depth,
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

        if is_terminal(board):
            break

        current = WHITE if current == BLACK else BLACK

    total_time = time.perf_counter() - game_start
    winner = get_winner(board)

    return GameResult(
        winner=winner,
        moves=move_count,
        total_time=total_time,

        black_depth=black_depth,
        white_depth=white_depth,

        black_avg_time=average(black_times),
        white_avg_time=average(white_times),

        black_avg_nodes=average(black_nodes),
        white_avg_nodes=average(white_nodes),
    )


def print_game_result(result: GameResult, game_index: int, total_games: int) -> None:
    """
    Print one benchmark game result.
    """
    print("\n----------------------------------------")
    print(f"Game {game_index}/{total_games}")
    print(f"Black: depth {result.black_depth}")
    print(f"White: depth {result.white_depth}")
    print(f"Winner color: {winner_to_text(result.winner)}")
    print(f"Winner depth: {depth_winner_text(result)}")
    print(f"Moves: {result.moves}")
    print(f"Total time: {result.total_time:.4f}s")

    print(
        f"Black depth {result.black_depth} | "
        f"avg time/move={result.black_avg_time:.4f}s | "
        f"avg nodes/move={result.black_avg_nodes:.1f}"
    )

    print(
        f"White depth {result.white_depth} | "
        f"avg time/move={result.white_avg_time:.4f}s | "
        f"avg nodes/move={result.white_avg_nodes:.1f}"
    )


# ============================================================
# Depth benchmark
# ============================================================

def benchmark_depths() -> None:
    """
    Benchmark selected depths.

    For each pair of depths:
    - Game 1: depth A as black, depth B as white
    - Game 2: depth B as black, depth A as white

    This swaps first player advantage.
    """
    print("\nDepth benchmark mode")
    print("This mode compares selected search depths.")
    print("Each matchup is played twice: once with each depth starting first.")

    depths = ask_depth_list()

    games_per_side = ask_positive_int(
        "\nHow many games for each side order? "
        "Example: 1 means A-black/B-white once and B-black/A-white once: "
    )

    max_moves = ask_int(
        "Max moves per game? Choose 60, 100, 120, or 225: ",
        [60, 100, 120, 225],
    )

    score_by_depth: Dict[int, float] = {d: 0.0 for d in depths}
    games_by_depth: Dict[int, int] = {d: 0 for d in depths}
    time_by_depth: Dict[int, List[float]] = {d: [] for d in depths}
    nodes_by_depth: Dict[int, List[float]] = {d: [] for d in depths}

    matchups: List[Tuple[int, int]] = []

    for i in range(len(depths)):
        for j in range(i + 1, len(depths)):
            d1 = depths[i]
            d2 = depths[j]

            for _ in range(games_per_side):
                matchups.append((d1, d2))
                matchups.append((d2, d1))

    total_games = len(matchups)

    print("\nRunning benchmark...")
    print(f"Selected depths: {depths}")
    print(f"Total games: {total_games}")

    for index, (black_depth, white_depth) in enumerate(matchups, start=1):
        result = play_ai_game_silent(
            black_depth=black_depth,
            white_depth=white_depth,
            max_moves=max_moves,
        )

        print_game_result(result, index, total_games)

        # Score by depth
        if result.winner == 1:
            score_by_depth[result.black_depth] += 1.0
            score_by_depth[result.white_depth] += 0.0
        elif result.winner == -1:
            score_by_depth[result.black_depth] += 0.0
            score_by_depth[result.white_depth] += 1.0
        else:
            score_by_depth[result.black_depth] += 0.5
            score_by_depth[result.white_depth] += 0.5

        games_by_depth[result.black_depth] += 1
        games_by_depth[result.white_depth] += 1

        time_by_depth[result.black_depth].append(result.black_avg_time)
        time_by_depth[result.white_depth].append(result.white_avg_time)

        nodes_by_depth[result.black_depth].append(result.black_avg_nodes)
        nodes_by_depth[result.white_depth].append(result.white_avg_nodes)

    print("\n========== Depth Benchmark Summary ==========")
    print(
        f"{'Depth':<8}"
        f"{'Games':<8}"
        f"{'Score':<10}"
        f"{'Quality %':<12}"
        f"{'Avg time/move':<18}"
        f"{'Avg nodes/move':<18}"
    )

    best_depth = None
    best_combined_score = float("-inf")

    for depth in depths:
        games = games_by_depth[depth]
        score = score_by_depth[depth]

        quality = score / games if games > 0 else 0.0
        avg_time = average(time_by_depth[depth])
        avg_nodes = average(nodes_by_depth[depth])

        # Quality-time balance.
        # Larger quality is better.
        # Larger time is slightly penalized.
        combined_score = quality - 0.05 * avg_time

        if combined_score > best_combined_score:
            best_combined_score = combined_score
            best_depth = depth

        print(
            f"{depth:<8}"
            f"{games:<8}"
            f"{score:<10.2f}"
            f"{quality * 100:<12.1f}"
            f"{avg_time:<18.4f}"
            f"{avg_nodes:<18.1f}"
        )

    print("\nRecommended depth:", best_depth)
    print("Reason: best balance between decision quality and thinking time.")


# ============================================================
# Menu
# ============================================================

def main_menu() -> None:
    """Main menu."""
    while True:
        print("\n===================================")
        print("           Gomoku AI Menu")
        print("===================================")
        print("1. Human vs AI")
        print("2. AI vs AI")
        print("3. Depth benchmark")
        print("4. Quit")

        choice = ask_int("Choose mode: ", [1, 2, 3, 4])

        if choice == 1:
            play_human_vs_ai()

        elif choice == 2:
            play_ai_vs_ai()

        elif choice == 3:
            benchmark_depths()

        elif choice == 4:
            print("Goodbye.")
            return


if __name__ == "__main__":
    main_menu()