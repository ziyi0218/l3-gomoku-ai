import random
import time
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict, Callable

from game.board import Board
from game.rules import (
    is_terminal,
    get_winner,
    generate_candidate_moves,
    find_winning_line,
)
from game.utils import print_board

from ai.minmax import choose_move_minimax
from ai.evaluation import (
    eval_basic,
    eval_intermediate,
    eval_advanced,
)

Move = Tuple[int, int]
EvalFn = Callable[[Board, int], float]


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

    black_eval_name: str
    white_eval_name: str

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


def ask_evaluation() -> Tuple[EvalFn, str]:
    """
    Ask user to choose an evaluation function.
    """
    print("\nChoose evaluation function:")
    print("1. Eval A - consecutive segment length")
    print("2. Eval B - segment length + open ends")
    print("3. Eval C - five-cell window potential")

    choice = ask_int("Your choice: ", [1, 2, 3])

    if choice == 1:
        return eval_basic, "Eval A"
    elif choice == 2:
        return eval_intermediate, "Eval B"
    else:
        return eval_advanced, "Eval C"


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
        return f"Depth {result.black_depth} ({result.black_eval_name})"
    if result.winner == -1:
        return f"Depth {result.white_depth} ({result.white_eval_name})"
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
    eval_fn: EvalFn,
) -> Tuple[Move, MoveStats]:
    """
    Choose one move with Minimax and measure time + nodes.
    """
    start = time.perf_counter()

    move, stats = choose_move_minimax(
        board=board,
        player=player,
        depth=depth,
        eval_fn=eval_fn,
    )

    elapsed = time.perf_counter() - start

    if move is None:
        move = ai_move_random(board)

    return move, MoveStats(
        time_seconds=elapsed,
        nodes=stats.nodes_evaluated,
    )


def ai_move_minimax(
    board: Board,
    player: int,
    depth: int,
    eval_fn: EvalFn,
    eval_name: str,
) -> Move:
    """
    Visible AI move for normal play mode.
    """
    move, stats = ai_move_minimax_with_stats(
        board=board,
        player=player,
        depth=depth,
        eval_fn=eval_fn,
    )

    print(
        f"AI stats | depth={depth} | eval={eval_name} | "
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

    print("\nChoose evaluation for AI:")
    eval_fn, eval_name = ask_evaluation()

    print("\nHuman vs AI started.")
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
            r, c = ai_move_minimax(
                board=board,
                player=AI,
                depth=depth,
                eval_fn=eval_fn,
                eval_name=eval_name,
            )

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
    """AI vs AI mode with depth and evaluation selection."""
    board = Board(15)

    AI1 = 1
    AI2 = -1

    print("\nAI vs AI mode.")

    print("\nChoose depth for AI1:")
    depth_ai1 = ask_depth()

    print("\nChoose evaluation for AI1:")
    eval_ai1, eval_name_ai1 = ask_evaluation()

    print("\nChoose depth for AI2:")
    depth_ai2 = ask_depth()

    print("\nChoose evaluation for AI2:")
    eval_ai2, eval_name_ai2 = ask_evaluation()

    current = AI1
    move_count = 0

    print("\nAI vs AI started.\n")
    print(f"AI1 = Black, depth {depth_ai1}, {eval_name_ai1}")
    print(f"AI2 = White, depth {depth_ai2}, {eval_name_ai2}\n")

    print_board(board)

    while True:
        if current == AI1:
            depth = depth_ai1
            eval_fn = eval_ai1
            eval_name = eval_name_ai1
            ai_name = "AI1"
        else:
            depth = depth_ai2
            eval_fn = eval_ai2
            eval_name = eval_name_ai2
            ai_name = "AI2"

        r, c = ai_move_minimax(
            board=board,
            player=current,
            depth=depth,
            eval_fn=eval_fn,
            eval_name=eval_name,
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


# ============================================================
# Benchmark game
# ============================================================

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


def print_game_result(result: GameResult, game_index: int, total_games: int) -> None:
    """
    Print one benchmark game result.
    """
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
    Benchmark different depths using the same evaluation function.

    The evaluation function is fixed.
    Only the search depth changes.

    For each pair of depths:
    - Game 1: depth A as black, depth B as white
    - Game 2: depth B as black, depth A as white

    This swaps first-player advantage.
    """
    print("\nDepth benchmark mode")
    print("This mode compares search depths using the same evaluation function.")
    print("Only depth changes. Evaluation is fixed for all AIs.")

    depths = ask_depth_list()

    print("\nChoose the evaluation function used for all depths:")
    eval_fn, eval_name = ask_evaluation()

    games_per_side = ask_positive_int(
        "\nHow many games for each side order? "
        "Example: 1 means A-black/B-white once and B-black/A-white once: "
    )

    max_moves = ask_int(
        "Max moves per game? Choose 60, 100, 120, or 225: ",
        [60, 100, 120, 225],
    )

    print_each_step_choice = ask_int(
        "Print board after each move? 1 = yes, 2 = no: ",
        [1, 2],
    )
    print_each_step = print_each_step_choice == 1

    print_final_boards_choice = ask_int(
        "Print final board after each game? 1 = yes, 2 = no: ",
        [1, 2],
    )
    print_final_boards = print_final_boards_choice == 1

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

    print("\nRunning depth benchmark...")
    print(f"Selected depths: {depths}")
    print(f"Fixed evaluation: {eval_name}")
    print(f"Total games: {total_games}")

    for index, (black_depth, white_depth) in enumerate(matchups, start=1):
        print("\n========================================")
        print(f"Benchmark game {index}/{total_games}")
        print(f"Black: depth {black_depth}, {eval_name}")
        print(f"White: depth {white_depth}, {eval_name}")
        print("========================================")

        result = run_one_benchmark_game(
            black_depth=black_depth,
            white_depth=white_depth,
            black_eval_fn=eval_fn,
            white_eval_fn=eval_fn,
            black_eval_name=eval_name,
            white_eval_name=eval_name,
            max_moves=max_moves,
            print_final_board=print_final_boards,
            print_each_step=print_each_step,
        )

        print_game_result(result, index, total_games)

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
    print(f"Fixed evaluation: {eval_name}")
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
# Evaluation benchmark
# ============================================================

def benchmark_evaluations() -> None:
    """
    Compare Eval A, Eval B, Eval C under the same depth.
    """
    print("\nEvaluation benchmark mode")
    print("This mode compares Eval A, Eval B, and Eval C under the same depth.")

    depth = ask_depth()

    games_per_side = ask_positive_int(
        "\nHow many games for each side order? "
        "Example: 1 means A-black/B-white once and B-black/A-white once: "
    )

    max_moves = ask_int(
        "Max moves per game? Choose 60, 100, 120, or 225: ",
        [60, 100, 120, 225],
    )

    print_each_step_choice = ask_int(
        "Print board after each move? 1 = yes, 2 = no: ",
        [1, 2],
    )
    print_each_step = print_each_step_choice == 1

    print_final_boards_choice = ask_int(
        "Print final board after each game? 1 = yes, 2 = no: ",
        [1, 2],
    )
    print_final_boards = print_final_boards_choice == 1

    evals: List[Tuple[str, EvalFn]] = [
        ("Eval A", eval_basic),
        ("Eval B", eval_intermediate),
        ("Eval C", eval_advanced),
    ]

    score_by_eval: Dict[str, float] = {name: 0.0 for name, _ in evals}
    games_by_eval: Dict[str, int] = {name: 0 for name, _ in evals}
    time_by_eval: Dict[str, List[float]] = {name: [] for name, _ in evals}
    nodes_by_eval: Dict[str, List[float]] = {name: [] for name, _ in evals}

    matchups: List[Tuple[str, EvalFn, str, EvalFn]] = []

    for i in range(len(evals)):
        for j in range(i + 1, len(evals)):
            name1, fn1 = evals[i]
            name2, fn2 = evals[j]

            for _ in range(games_per_side):
                matchups.append((name1, fn1, name2, fn2))
                matchups.append((name2, fn2, name1, fn1))

    total_games = len(matchups)

    print("\nRunning evaluation benchmark...")
    print(f"Depth: {depth}")
    print(f"Total games: {total_games}")

    for index, (black_eval_name, black_eval_fn, white_eval_name, white_eval_fn) in enumerate(matchups, start=1):
        print("\n========================================")
        print(f"Evaluation benchmark game {index}/{total_games}")
        print(f"Black: {black_eval_name}, depth {depth}")
        print(f"White: {white_eval_name}, depth {depth}")
        print("========================================")

        result = run_one_benchmark_game(
            black_depth=depth,
            white_depth=depth,
            black_eval_fn=black_eval_fn,
            white_eval_fn=white_eval_fn,
            black_eval_name=black_eval_name,
            white_eval_name=white_eval_name,
            max_moves=max_moves,
            print_final_board=print_final_boards,
            print_each_step=print_each_step,
        )

        print_game_result(result, index, total_games)

        if result.winner == 1:
            score_by_eval[result.black_eval_name] += 1.0
            score_by_eval[result.white_eval_name] += 0.0
        elif result.winner == -1:
            score_by_eval[result.black_eval_name] += 0.0
            score_by_eval[result.white_eval_name] += 1.0
        else:
            score_by_eval[result.black_eval_name] += 0.5
            score_by_eval[result.white_eval_name] += 0.5

        games_by_eval[result.black_eval_name] += 1
        games_by_eval[result.white_eval_name] += 1

        time_by_eval[result.black_eval_name].append(result.black_avg_time)
        time_by_eval[result.white_eval_name].append(result.white_avg_time)

        nodes_by_eval[result.black_eval_name].append(result.black_avg_nodes)
        nodes_by_eval[result.white_eval_name].append(result.white_avg_nodes)

    print("\n========== Evaluation Benchmark Summary ==========")
    print(
        f"{'Eval':<10}"
        f"{'Games':<8}"
        f"{'Score':<10}"
        f"{'Quality %':<12}"
        f"{'Avg time/move':<18}"
        f"{'Avg nodes/move':<18}"
    )

    best_eval = None
    best_quality = float("-inf")

    for eval_name, _ in evals:
        games = games_by_eval[eval_name]
        score = score_by_eval[eval_name]

        quality = score / games if games > 0 else 0.0
        avg_time = average(time_by_eval[eval_name])
        avg_nodes = average(nodes_by_eval[eval_name])

        if quality > best_quality:
            best_quality = quality
            best_eval = eval_name

        print(
            f"{eval_name:<10}"
            f"{games:<8}"
            f"{score:<10.2f}"
            f"{quality * 100:<12.1f}"
            f"{avg_time:<18.4f}"
            f"{avg_nodes:<18.1f}"
        )

    print("\nRecommended evaluation:", best_eval)


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
        print("4. Evaluation benchmark")
        print("5. Quit")

        choice = ask_int("Choose mode: ", [1, 2, 3, 4, 5])

        if choice == 1:
            play_human_vs_ai()

        elif choice == 2:
            play_ai_vs_ai()

        elif choice == 3:
            benchmark_depths()

        elif choice == 4:
            benchmark_evaluations()

        elif choice == 5:
            print("Goodbye.")
            return


if __name__ == "__main__":
    main_menu()