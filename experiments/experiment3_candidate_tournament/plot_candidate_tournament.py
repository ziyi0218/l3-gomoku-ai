import csv
import argparse
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

RESULT_DIR = Path("experiments/experiment3_candidate_tournament/results")


def load_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def require_matplotlib():
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit(
            "matplotlib is required for plotting. Install it with requirements.txt."
        ) from exc
    return plt


def plot_bar(rows, field: str, output_name: str, ylabel: str) -> None:
    plt = require_matplotlib()
    sorted_rows = sorted(rows, key=lambda row: row["ai"])
    labels = [row["ai"] for row in sorted_rows]
    values = [float(row[field]) for row in sorted_rows]

    plt.bar(labels, values)
    plt.xlabel("Candidate AI")
    plt.ylabel(ylabel)
    plt.title(ylabel + " by candidate AI")
    plt.grid(axis="y", alpha=0.3)
    plt.savefig(RESULT_DIR / output_name, dpi=160, bbox_inches="tight")
    plt.close()


def plot_strength_vs_time(rows) -> None:
    plt = require_matplotlib()
    for row in rows:
        x = float(row["avg_time_per_move_ms"])
        y = float(row["score_rate"])
        plt.scatter(x, y)
        plt.annotate(row["ai"], (x, y), textcoords="offset points", xytext=(5, 5))

    plt.xlabel("Average time per move (ms)")
    plt.ylabel("Score rate")
    plt.title("Strength-runtime trade-off")
    plt.grid(True, alpha=0.3)
    plt.savefig(RESULT_DIR / "candidate_strength_vs_time.png", dpi=160, bbox_inches="tight")
    plt.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot Experiment 3 candidate tournament results.")
    parser.add_argument("--results-dir", type=Path, default=RESULT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results_dir = args.results_dir
    results_dir.mkdir(parents=True, exist_ok=True)
    rows = load_rows(results_dir / "candidate_ai_ranking.csv")
    global RESULT_DIR
    RESULT_DIR = results_dir
    plot_bar(rows, "win_rate", "candidate_win_rate.png", "Win rate")
    plot_bar(rows, "avg_time_per_move_ms", "candidate_avg_time.png", "Average time per move (ms)")
    plot_strength_vs_time(rows)
    print(f"Wrote plots to {results_dir}")


if __name__ == "__main__":
    main()
