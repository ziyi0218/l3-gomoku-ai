import argparse
import csv
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai.alphabeta import choose_move_alphabeta
from ai.evaluation import eval_intermediate
from ai.minmax import choose_move_minimax
from experiments.experiment1_search.positions import FIXED_POSITIONS, FixedPosition
from game.rules import generate_candidate_moves, get_winner, is_terminal

Move = Tuple[int, int]

EVAL_NAME = "Eval B / intermediate"
RESULT_DIR = Path("experiments/experiment1_search/results")
DETAIL_CSV = RESULT_DIR / "search_benchmark.csv"
SUMMARY_CSV = RESULT_DIR / "search_benchmark_summary.csv"
SUMMARY_MD = RESULT_DIR / "search_benchmark_summary.md"


@dataclass(frozen=True)
class AlgorithmCase:
    algorithm: str
    ordering: str


ALGORITHMS = [
    AlgorithmCase("Minimax", "none"),
    AlgorithmCase("Alpha-Beta", "off"),
    AlgorithmCase("Alpha-Beta", "on"),
]


def board_signature(board) -> Tuple[Tuple[int, ...], ...]:
    return tuple(tuple(row) for row in board.grid)


def format_move(move: Optional[Move]) -> str:
    if move is None:
        return ""
    return f"{move[0]} {move[1]}"


def scores_equal(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)


def run_search(position: FixedPosition, depth: int, case: AlgorithmCase):
    board = position.make_board()
    before = board_signature(board)

    if case.algorithm == "Minimax":
        move, score, stats = choose_move_minimax(
            board=board,
            player=position.player_to_move,
            depth=depth,
            eval_fn=eval_intermediate,
        )
    else:
        move, score, stats = choose_move_alphabeta(
            board=board,
            player=position.player_to_move,
            depth=depth,
            eval_fn=eval_intermediate,
            use_ordering=case.ordering == "on",
        )

    after = board_signature(board)
    if before != after:
        raise RuntimeError(
            f"Board state was modified by search: {position.name}, depth {depth}, {case}"
        )

    return move, score, stats


def run_average(position: FixedPosition, depth: int, case: AlgorithmCase, repeats: int):
    first_move = None
    first_score = None
    first_nodes = None
    first_cutoffs = None
    first_candidate_count = None
    total_time_ms = 0.0

    for run_id in range(1, repeats + 1):
        move, score, stats = run_search(position, depth, case)

        if run_id == 1:
            first_move = move
            first_score = score
            first_nodes = stats.nodes
            first_cutoffs = stats.cutoffs if hasattr(stats, "cutoffs") else 0
            first_candidate_count = stats.candidate_count
        else:
            if move != first_move or not scores_equal(score, first_score):
                raise RuntimeError(
                    "Non-deterministic search result for "
                    f"{position.name}, depth {depth}, {case}: "
                    f"first={(first_move, first_score)}, current={(move, score)}"
                )

        total_time_ms += stats.time_ms

    return {
        "move": first_move,
        "score": first_score,
        "nodes": first_nodes,
        "cutoffs": first_cutoffs,
        "candidate_count": first_candidate_count,
        "time_ms": total_time_ms / repeats,
    }


def build_detail_rows(
    positions: Iterable[FixedPosition],
    depths: Iterable[int],
    repeats: int,
) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []

    for position in positions:
        board = position.make_board()
        terminal = is_terminal(board)
        winner = get_winner(board)
        base_candidates = generate_candidate_moves(board, radius=2)

        for depth in depths:
            baseline = run_average(position, depth, ALGORITHMS[0], repeats)

            for case in ALGORITHMS:
                result = baseline if case.algorithm == "Minimax" else run_average(
                    position, depth, case, repeats
                )

                same_score = scores_equal(result["score"], baseline["score"])
                same_move = result["move"] == baseline["move"]

                rows.append(
                    {
                        "position": position.name,
                        "description": position.description,
                        "expected_property": position.expected_property,
                        "player_to_move": position.player_to_move,
                        "terminal_before_search": terminal,
                        "winner_before_search": winner if winner is not None else "",
                        "depth": depth,
                        "algorithm": case.algorithm,
                        "ordering": case.ordering,
                        "eval": EVAL_NAME,
                        "candidate_rule": "generate_candidate_moves(radius=2)",
                        "root_candidate_count": len(base_candidates),
                        "best_move": format_move(result["move"]),
                        "best_score": result["score"],
                        "nodes": result["nodes"],
                        "cutoffs": result["cutoffs"],
                        "time_ms": round(result["time_ms"], 4),
                        "candidate_count": result["candidate_count"],
                        "same_score_with_minimax": same_score,
                        "same_move_with_minimax": same_move,
                        "runs": repeats,
                    }
                )

    return rows


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("No rows to write")

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_summary_rows(detail_rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    grouped = defaultdict(list)
    minimax_nodes_by_depth: Dict[int, float] = {}

    for row in detail_rows:
        key = (int(row["depth"]), str(row["algorithm"]), str(row["ordering"]))
        grouped[key].append(row)

    for key, rows in grouped.items():
        depth, algorithm, _ = key
        if algorithm == "Minimax":
            minimax_nodes_by_depth[depth] = average_float(rows, "nodes")

    summary = []

    for key in sorted(grouped):
        depth, algorithm, ordering = key
        rows = grouped[key]
        avg_nodes = average_float(rows, "nodes")
        base_nodes = minimax_nodes_by_depth.get(depth, avg_nodes)
        reduction = 0.0 if base_nodes == 0 else 1 - avg_nodes / base_nodes

        summary.append(
            {
                "depth": depth,
                "algorithm": algorithm,
                "ordering": ordering,
                "positions": len(rows),
                "avg_nodes": round(avg_nodes, 2),
                "avg_time_ms": round(average_float(rows, "time_ms"), 4),
                "avg_cutoffs": round(average_float(rows, "cutoffs"), 2),
                "node_reduction_vs_minimax": round(reduction, 4),
                "score_matches_minimax": sum(
                    1 for row in rows if str(row["same_score_with_minimax"]) == "True"
                ),
                "move_matches_minimax": sum(
                    1 for row in rows if str(row["same_move_with_minimax"]) == "True"
                ),
            }
        )

    return summary


def average_float(rows: List[Dict[str, object]], field: str) -> float:
    return sum(float(row[field]) for row in rows) / len(rows)


def write_summary_markdown(path: Path, summary_rows: List[Dict[str, object]]) -> None:
    headers = [
        "depth",
        "algorithm",
        "ordering",
        "avg_nodes",
        "avg_time_ms",
        "avg_cutoffs",
        "node_reduction_vs_minimax",
        "score_matches_minimax",
        "move_matches_minimax",
    ]

    lines = [
        "# Experiment 1 Search Benchmark Summary",
        "",
        "Fixed evaluation: Eval B / intermediate.",
        "Candidate rule: generate_candidate_moves(radius=2).",
        "",
        "|" + "|".join(headers) + "|",
        "|" + "|".join(["---"] * len(headers)) + "|",
    ]

    for row in summary_rows:
        lines.append("|" + "|".join(str(row[h]) for h in headers) + "|")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Experiment 1: Minimax vs Alpha-Beta pruning benchmark."
    )
    parser.add_argument("--depths", nargs="+", type=int, default=[1, 2, 3])
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--output", type=Path, default=DETAIL_CSV)
    parser.add_argument("--summary-output", type=Path, default=SUMMARY_CSV)
    parser.add_argument("--summary-md", type=Path, default=SUMMARY_MD)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.repeats <= 0:
        raise ValueError("--repeats must be positive")

    detail_rows = build_detail_rows(FIXED_POSITIONS, args.depths, args.repeats)
    write_csv(args.output, detail_rows)

    summary_rows = build_summary_rows(detail_rows)
    write_csv(args.summary_output, summary_rows)
    write_summary_markdown(args.summary_md, summary_rows)

    print(f"Wrote detail CSV: {args.output}")
    print(f"Wrote summary CSV: {args.summary_output}")
    print(f"Wrote summary Markdown: {args.summary_md}")


if __name__ == "__main__":
    main()
