from typing import Dict, List, Tuple

from ai.evaluation import eval_advanced, eval_basic, eval_intermediate
from cli.input import ask_depth, ask_int, ask_positive_int
from cli.output import average, print_game_result
from experiments.benchmark import run_one_benchmark_game
from models import EvalFn


def benchmark_evaluations() -> None:
    """Compare Eval A, Eval B, Eval C under the same depth."""
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

    for index, (
        black_eval_name,
        black_eval_fn,
        white_eval_name,
        white_eval_fn,
    ) in enumerate(matchups, start=1):
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
