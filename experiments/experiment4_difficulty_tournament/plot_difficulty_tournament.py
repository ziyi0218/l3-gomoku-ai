import argparse
import csv
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

RESULT_DIR = Path("experiments/experiment4_difficulty_tournament/result12")

DIFFICULTY_ORDER = {
    "Easy": 0,
    "Medium": 1,
    "Hard": 2,
}


def load_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as file_obj:
        return list(csv.DictReader(file_obj))


def require_matplotlib():
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit(
            "matplotlib is required for plotting. Install it with requirements.txt."
        ) from exc
    return plt


def game_score_for_ai(game, ai_name):
    if game["winner"] == "draw":
        return 0.5
    return 1.0 if game["winner_ai"] == ai_name else 0.0


def canonical_pair(ai_a, ai_b):
    ordered = sorted((ai_a, ai_b), key=lambda name: DIFFICULTY_ORDER[name])
    return ordered[0], ordered[1]


def build_balanced_game_order(games, ai_1, ai_2):
    first_side = []
    second_side = []

    for game in sorted(games, key=lambda row: int(row["game_id"])):
        if game["black_ai"] == ai_1 and game["white_ai"] == ai_2:
            first_side.append(game)
        elif game["black_ai"] == ai_2 and game["white_ai"] == ai_1:
            second_side.append(game)
        else:
            raise ValueError(f"Unexpected game pairing: {game['black_ai']} vs {game['white_ai']}")

    ordered_games = []
    for index in range(max(len(first_side), len(second_side))):
        if index < len(first_side):
            ordered_games.append(first_side[index])
        if index < len(second_side):
            ordered_games.append(second_side[index])

    return ordered_games


def build_cumulative_score_rates(rows):
    grouped = {}
    for row in rows:
        pair_key = canonical_pair(row["black_ai"], row["white_ai"])
        grouped.setdefault(pair_key, []).append(row)

    series = {}
    for pair_key, games in grouped.items():
        weaker_ai, stronger_ai = pair_key
        tracked_ai = stronger_ai
        ordered_games = build_balanced_game_order(games, weaker_ai, stronger_ai)
        cumulative_rates = []
        tracked_score = 0.0

        for index, game in enumerate(ordered_games, start=1):
            tracked_score += game_score_for_ai(game, tracked_ai)
            cumulative_rates.append(100.0 * tracked_score / index)

        series[pair_key] = cumulative_rates

    return series


def format_pair_label(pair_key):
    weaker_ai, stronger_ai = pair_key
    french_names = {
        "Easy": "Facile",
        "Medium": "Moyen",
        "Hard": "Difficile",
    }
    return f"{french_names[stronger_ai]} vs {french_names[weaker_ai]}"


def final_rate_text(values):
    if not values:
        return "0.0%"
    return f"{values[-1]:.1f}%"


def sorted_ranking_rows(rows):
    return sorted(rows, key=lambda row: DIFFICULTY_ORDER[row["ai"]])


def plot_bar(rows, field: str, output_name: str, ylabel: str, title: str) -> None:
    plt = require_matplotlib()
    sorted_rows = sorted_ranking_rows(rows)
    labels = [row["ai"] for row in sorted_rows]
    values = [float(row[field]) for row in sorted_rows]
    colors = ["tab:green", "tab:orange", "tab:red"]

    fig, ax = plt.subplots(figsize=(8, 4.8))
    bars = ax.bar(labels, values, color=colors)
    ax.set_xlabel("Difficulty AI")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.3)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.4g}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.savefig(RESULT_DIR / output_name, dpi=170, bbox_inches="tight")
    plt.close(fig)


def plot_color_win_rates(rows, results_dir: Path) -> None:
    plt = require_matplotlib()
    sorted_rows = sorted_ranking_rows(rows)
    labels = [row["ai"] for row in sorted_rows]
    black_rates = [float(row["black_win_rate"]) for row in sorted_rows]
    white_rates = [float(row["white_win_rate"]) for row in sorted_rows]
    x_values = range(len(labels))
    width = 0.36

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.bar([x - width / 2 for x in x_values], black_rates, width, label="Black win rate")
    ax.bar([x + width / 2 for x in x_values], white_rates, width, label="White win rate")
    ax.set_xticks(list(x_values))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Difficulty AI")
    ax.set_ylabel("Win rate")
    ax.set_title("Black vs white win rate")
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    fig.savefig(results_dir / "difficulty_color_win_rate.png", dpi=170, bbox_inches="tight")
    plt.close(fig)


def plot_strength_vs_time(rows, results_dir: Path) -> None:
    plt = require_matplotlib()
    fig, ax = plt.subplots(figsize=(8.5, 5.2))

    for row in sorted_ranking_rows(rows):
        x = float(row["avg_time_per_move_ms"])
        y = float(row["score_rate"])
        ax.scatter(x, y, s=85)
        ax.annotate(row["ai"], (x, y), textcoords="offset points", xytext=(6, 6))

    ax.set_xlabel("Average time per move (ms)")
    ax.set_ylabel("Score rate")
    ax.set_title("Difficulty strength-runtime trade-off")
    ax.grid(True, alpha=0.3)
    fig.savefig(results_dir / "difficulty_strength_vs_time.png", dpi=170, bbox_inches="tight")
    plt.close(fig)


def pairwise_score_for(rows, ai_row: str, ai_col: str) -> float:
    if ai_row == ai_col:
        return 0.5

    for row in rows:
        ai_1 = row["ai_1"]
        ai_2 = row["ai_2"]
        if ai_row == ai_1 and ai_col == ai_2:
            return float(row["ai_1_score_rate"])
        if ai_row == ai_2 and ai_col == ai_1:
            return float(row["ai_2_score_rate"])

    raise ValueError(f"Missing pairwise row for {ai_row} vs {ai_col}")


def plot_pairwise_score_heatmap(rows, results_dir: Path) -> None:
    plt = require_matplotlib()
    labels = sorted(DIFFICULTY_ORDER, key=DIFFICULTY_ORDER.get)
    matrix = [
        [pairwise_score_for(rows, row_label, col_label) for col_label in labels]
        for row_label in labels
    ]

    fig, ax = plt.subplots(figsize=(6.5, 5.4))
    image = ax.imshow(matrix, vmin=0, vmax=1, cmap="RdYlGn")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.set_xlabel("Opponent")
    ax.set_ylabel("AI")
    ax.set_title("Pairwise score rate heatmap")

    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            ax.text(c, r, f"{value:.3f}", ha="center", va="center", color="black")

    fig.colorbar(image, ax=ax, label="Score rate")
    fig.savefig(results_dir / "difficulty_pairwise_score_heatmap.png", dpi=170, bbox_inches="tight")
    plt.close(fig)


def plot_pairwise_results(rows, results_dir: Path) -> None:
    plt = require_matplotlib()
    labels = []
    lower_wins = []
    draws = []
    higher_wins = []

    for row in rows:
        ai_1 = row["ai_1"]
        ai_2 = row["ai_2"]
        labels.append(f"{ai_1} vs {ai_2}")
        lower_wins.append(int(row["ai_1_wins"]))
        draws.append(int(row["draws"]))
        higher_wins.append(int(row["ai_2_wins"]))

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(labels, lower_wins, label="ai_1 wins")
    ax.bar(labels, draws, bottom=lower_wins, label="draws")
    bottoms = [win + draw for win, draw in zip(lower_wins, draws)]
    ax.bar(labels, higher_wins, bottom=bottoms, label="ai_2 wins")
    ax.set_xlabel("Pair")
    ax.set_ylabel("Games")
    ax.set_title("Pairwise results")
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    fig.autofmt_xdate(rotation=20, ha="right")
    fig.savefig(results_dir / "difficulty_pairwise_results.png", dpi=170, bbox_inches="tight")
    plt.close(fig)


def plot_cumulative_win_rates(rows, results_dir: Path) -> None:
    plt = require_matplotlib()
    series = build_cumulative_score_rates(rows)
    colors = ["tab:orange", "crimson", "cornflowerblue"]
    linestyles = ["-", "--", "-."]
    markers = ["o", "s", "^"]

    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    ax.axhline(50, color="gray", linestyle="--", linewidth=1.2, alpha=0.7, label="50 %")

    ordered_keys = sorted(series.keys(), key=lambda pair: (DIFFICULTY_ORDER[pair[1]], DIFFICULTY_ORDER[pair[0]]))

    for index, (color, pair_key) in enumerate(zip(colors, ordered_keys)):
        values = series[pair_key]
        x_values = list(range(1, len(values) + 1))
        label_prefix = format_pair_label(pair_key)
        ax.plot(
            x_values,
            values,
            color=color,
            linewidth=2.0,
            linestyle=linestyles[index % len(linestyles)],
            marker=markers[index % len(markers)],
            markersize=3.0,
            markevery=max(1, len(values) // 20),
            alpha=0.9,
            zorder=3 + index,
            label=f"{label_prefix}  ->  {final_rate_text(values)}",
        )

    ax.set_xscale("log")
    ax.set_xlim(1, max(len(values) for values in series.values()))
    ax.set_ylim(0, 100)
    ax.set_xlabel("Nombre de parties (echelle log)")
    ax.set_ylabel("Taux de score cumule (%)")
    ax.set_title("Evolution du score cumule selon les paires d'IA")
    ax.grid(True, which="both", linestyle="--", alpha=0.35)
    ax.legend(loc="lower left", frameon=True)

    output_path = results_dir / "difficulty_cumulative_blue_win_rate.png"
    fig.savefig(output_path, dpi=170, bbox_inches="tight")
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot Experiment 4 difficulty tournament results.")
    parser.add_argument("--results-dir", type=Path, default=RESULT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results_dir = args.results_dir
    match_results_path = results_dir / "difficulty_match_results.csv"
    ranking_path = results_dir / "difficulty_ai_ranking.csv"
    pairwise_path = results_dir / "difficulty_pairwise_summary.csv"

    if not match_results_path.exists():
        raise SystemExit(f"Missing match results file: {match_results_path}")
    if not ranking_path.exists():
        raise SystemExit(f"Missing ranking file: {ranking_path}")
    if not pairwise_path.exists():
        raise SystemExit(f"Missing pairwise file: {pairwise_path}")

    rows = load_rows(match_results_path)
    ranking_rows = load_rows(ranking_path)
    pairwise_rows = load_rows(pairwise_path)

    plot_cumulative_win_rates(rows, results_dir)
    plot_strength_vs_time(ranking_rows, results_dir)
    plot_pairwise_score_heatmap(pairwise_rows, results_dir)
    plot_color_win_rates(ranking_rows, results_dir)
    print(f"Wrote plots to {results_dir}")


if __name__ == "__main__":
    main()
