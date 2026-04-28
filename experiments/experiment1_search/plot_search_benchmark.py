import csv
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

INPUT_CSV = Path("experiments/experiment1_search/results/search_benchmark_summary.csv")
OUTPUT_DIR = Path("experiments/experiment1_search/results")


def load_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def algorithm_label(row) -> str:
    if row["algorithm"] == "Minimax":
        return "Minimax"
    if row["ordering"] == "on":
        return "Alpha-Beta + ordering"
    return "Alpha-Beta"


def plot_metric(rows, metric: str, output_name: str, ylabel: str) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit(
            "matplotlib is required for plotting. Install it or use the CSV files directly."
        ) from exc

    by_algorithm = {}
    all_depths = set()
    for row in rows:
        label = algorithm_label(row)
        depth = int(row["depth"])
        all_depths.add(depth)
        by_algorithm.setdefault(label, []).append(
            (depth, float(row[metric]))
        )

    for label, values in by_algorithm.items():
        values.sort()
        plt.plot(
            [depth for depth, _ in values],
            [value for _, value in values],
            marker="o",
            label=label,
        )

    plt.xlabel("Search depth")
    plt.ylabel(ylabel)
    plt.title(ylabel + " vs depth")
    plt.xticks(sorted(all_depths))
    plt.legend()
    plt.grid(True, alpha=0.3)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_DIR / output_name, dpi=160, bbox_inches="tight")
    plt.close()


def main() -> None:
    rows = load_rows(INPUT_CSV)
    plot_metric(rows, "avg_nodes", "nodes_vs_depth.png", "Average explored nodes")
    plot_metric(rows, "avg_time_ms", "time_vs_depth.png", "Average time (ms)")
    plot_metric(rows, "avg_cutoffs", "cutoffs_vs_depth.png", "Average cutoffs")
    print(f"Wrote plots to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
