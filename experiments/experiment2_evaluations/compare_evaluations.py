import argparse
import csv
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai.alphabeta import ordered_moves, choose_move_alphabeta
from ai.evaluation import eval_advanced, eval_basic, eval_intermediate
from experiments.experiment2_evaluations.positions import (
    EVALUATION_POSITIONS,
    EvaluationPosition,
)
from game.rules import generate_candidate_moves, get_winner, is_terminal
from models import EvalFn

Move = Tuple[int, int]

RESULT_DIR = Path("experiments/experiment2_evaluations/results")
DETAIL_CSV = RESULT_DIR / "evaluation_comparison.csv"
SUMMARY_CSV = RESULT_DIR / "evaluation_comparison_summary.csv"
SUMMARY_MD = RESULT_DIR / "evaluation_comparison_summary.md"
MOVE_DIFF_CSV = RESULT_DIR / "evaluation_best_move_diff.csv"


@dataclass(frozen=True)
class EvaluationCase:
    name: str
    function: EvalFn
    description: str


EVALUATIONS = [
    EvaluationCase(
        "Eval A",
        eval_basic,
        "Consecutive segment length only.",
    ),
    EvaluationCase(
        "Eval B",
        eval_intermediate,
        "Segment length plus open/blocked ends.",
    ),
    EvaluationCase(
        "Eval C",
        eval_advanced,
        "Five-cell window potential plus center bonus.",
    ),
]


def board_signature(board) -> Tuple[Tuple[int, ...], ...]:
    return tuple(tuple(row) for row in board.grid)


def format_move(move: Optional[Move]) -> str:
    if move is None:
        return ""
    return f"{move[0]} {move[1]}"


def run_search(position: EvaluationPosition, depth: int, case: EvaluationCase):
    board = position.make_board()
    before = board_signature(board)
    base_moves = generate_candidate_moves(board, radius=2)
    ordered = ordered_moves(
        board=board,
        moves=base_moves,
        current_player=position.player_to_move,
        root_player=position.player_to_move,
        eval_fn=case.function,
    )

    if set(base_moves) != set(ordered):
        raise RuntimeError(
            f"Move ordering changed candidate set for {position.name}, {case.name}"
        )

    move, score, stats = choose_move_alphabeta(
        board=board,
        player=position.player_to_move,
        depth=depth,
        eval_fn=case.function,
        use_ordering=True,
    )

    after = board_signature(board)
    if before != after:
        raise RuntimeError(
            f"Board state was modified by search: {position.name}, depth {depth}, {case.name}"
        )

    if move is not None and move not in base_moves:
        raise RuntimeError(
            f"Illegal best move for {position.name}, depth {depth}, {case.name}: {move}"
        )

    return move, score, stats, len(base_moves)


def build_detail_rows(
    positions: Iterable[EvaluationPosition],
    depths: Iterable[int],
) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []

    for position in positions:
        board = position.make_board()
        terminal = is_terminal(board)
        winner = get_winner(board)

        for depth in depths:
            for case in EVALUATIONS:
                move, score, stats, candidate_count = run_search(position, depth, case)

                rows.append(
                    {
                        "position": position.name,
                        "description": position.description,
                        "purpose": position.purpose,
                        "player_to_move": position.player_to_move,
                        "terminal_before_search": terminal,
                        "winner_before_search": winner if winner is not None else "",
                        "depth": depth,
                        "search": "Alpha-Beta + ordering",
                        "evaluation": case.name,
                        "evaluation_description": case.description,
                        "candidate_rule": "generate_candidate_moves(radius=2)",
                        "best_move": format_move(move),
                        "best_score": score,
                        "nodes": stats.nodes,
                        "cutoffs": stats.cutoffs,
                        "time_ms": round(stats.time_ms, 4),
                        "candidate_count": candidate_count,
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


def average(rows: List[Dict[str, object]], field: str) -> float:
    return sum(float(row[field]) for row in rows) / len(rows)


def build_summary_rows(detail_rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    grouped = defaultdict(list)
    for row in detail_rows:
        key = (int(row["depth"]), str(row["evaluation"]))
        grouped[key].append(row)

    rows = []
    for depth, evaluation in sorted(grouped):
        items = grouped[(depth, evaluation)]
        rows.append(
            {
                "depth": depth,
                "evaluation": evaluation,
                "positions": len(items),
                "avg_time_ms": round(average(items, "time_ms"), 4),
                "avg_nodes": round(average(items, "nodes"), 2),
                "avg_cutoffs": round(average(items, "cutoffs"), 2),
                "avg_candidate_count": round(average(items, "candidate_count"), 2),
            }
        )
    return rows


def build_move_diff_rows(detail_rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    grouped = defaultdict(dict)
    for row in detail_rows:
        key = (str(row["position"]), int(row["depth"]))
        grouped[key][str(row["evaluation"])] = row

    rows = []
    for position, depth in sorted(grouped):
        items = grouped[(position, depth)]
        moves = {
            "Eval A": items["Eval A"]["best_move"],
            "Eval B": items["Eval B"]["best_move"],
            "Eval C": items["Eval C"]["best_move"],
        }
        unique_moves = set(moves.values())
        rows.append(
            {
                "position": position,
                "depth": depth,
                "EvalA_move": moves["Eval A"],
                "EvalB_move": moves["Eval B"],
                "EvalC_move": moves["Eval C"],
                "EvalA_score": items["Eval A"]["best_score"],
                "EvalB_score": items["Eval B"]["best_score"],
                "EvalC_score": items["Eval C"]["best_score"],
                "all_same": len(unique_moves) == 1,
                "moves_differ": len(unique_moves) > 1,
            }
        )
    return rows


def write_summary_markdown(path: Path, rows: List[Dict[str, object]]) -> None:
    headers = [
        "depth",
        "evaluation",
        "positions",
        "avg_time_ms",
        "avg_nodes",
        "avg_cutoffs",
        "avg_candidate_count",
    ]
    lines = [
        "# Experiment 2 Evaluation Comparison Summary",
        "",
        "Search: Alpha-Beta + move ordering.",
        "Depths: 1, 2, 3.",
        "Candidate rule: generate_candidate_moves(radius=2).",
        "",
        "|" + "|".join(headers) + "|",
        "|" + "|".join(["---"] * len(headers)) + "|",
    ]
    for row in rows:
        lines.append("|" + "|".join(str(row[h]) for h in headers) + "|")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Experiment 2: compare three evaluation functions."
    )
    parser.add_argument("--depths", nargs="+", type=int, default=[1, 2, 3])
    parser.add_argument("--output", type=Path, default=DETAIL_CSV)
    parser.add_argument("--summary-output", type=Path, default=SUMMARY_CSV)
    parser.add_argument("--summary-md", type=Path, default=SUMMARY_MD)
    parser.add_argument("--move-diff-output", type=Path, default=MOVE_DIFF_CSV)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if any(depth not in [1, 2, 3] for depth in args.depths):
        raise ValueError("Experiment 2 only supports depths 1, 2, and 3")

    detail_rows = build_detail_rows(EVALUATION_POSITIONS, args.depths)
    write_csv(args.output, detail_rows)

    summary_rows = build_summary_rows(detail_rows)
    write_csv(args.summary_output, summary_rows)
    write_summary_markdown(args.summary_md, summary_rows)

    move_diff_rows = build_move_diff_rows(detail_rows)
    write_csv(args.move_diff_output, move_diff_rows)

    differing = sum(1 for row in move_diff_rows if row["moves_differ"])
    print(f"Wrote detail CSV: {args.output}")
    print(f"Wrote summary CSV: {args.summary_output}")
    print(f"Wrote summary Markdown: {args.summary_md}")
    print(f"Wrote best-move difference CSV: {args.move_diff_output}")
    print(f"Best moves differ in {differing}/{len(move_diff_rows)} position-depth cases")


if __name__ == "__main__":
    main()
