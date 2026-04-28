from typing import Dict, List, Tuple

from cli.input import (
    ask_depth_list,
    ask_evaluation,
    ask_int,
    ask_positive_int,
    ask_search_algorithm,
)
from cli.output import average, print_game_result
from experiments.benchmark import run_one_benchmark_game


def benchmark_depths() -> None:
    """
    Benchmark different depths using the same evaluation function.

    The evaluation function is fixed.
    Only the search depth changes.
    """
    print("\nDepth benchmark mode")
    print("This mode compares search depths using the same evaluation function.")
    print("Only depth changes. Evaluation is fixed for all AIs.")

    depths = ask_depth_list()

    print("\nChoose the evaluation function used for all depths:")
    eval_fn, eval_name = ask_evaluation()

    print("\nChoose the search algorithm used for all depths:")
    search_name = ask_search_algorithm()

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
    print(f"Fixed search: {search_name}")
    print(f"Fixed evaluation: {eval_name}")
    print(f"Total games: {total_games}")

    for index, (black_depth, white_depth) in enumerate(matchups, start=1):
        print("\n========================================")
        print(f"Benchmark game {index}/{total_games}")
        print(f"Black: {search_name}, depth {black_depth}, {eval_name}")
        print(f"White: {search_name}, depth {white_depth}, {eval_name}")
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
            black_search_name=search_name,
            white_search_name=search_name,
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
    print(f"Fixed search: {search_name}")
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
