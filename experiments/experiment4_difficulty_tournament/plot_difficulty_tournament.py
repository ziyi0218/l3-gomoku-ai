import argparse
import csv
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

RESULT_DIR = Path("experiments/experiment4_difficulty_tournament/result7")


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
        pair_key = tuple(sorted((row["black_ai"], row["white_ai"])))
        grouped.setdefault(pair_key, []).append(row)

    series = {}
    for pair_key, games in grouped.items():
        ai_1, ai_2 = pair_key
        tracked_ai = ai_2
        ordered_games = build_balanced_game_order(games, ai_1, ai_2)
        cumulative_rates = []
        tracked_score = 0.0

        for index, game in enumerate(ordered_games, start=1):
            tracked_score += game_score_for_ai(game, tracked_ai)
            cumulative_rates.append(100.0 * tracked_score / index)

        series[pair_key] = cumulative_rates

    return series


def format_pair_label(pair_key):
    ai_1, ai_2 = pair_key
    french_names = {
        "Easy": "Facile",
        "Medium": "Moyen",
        "Hard": "Difficile",
    }
    return f"{french_names[ai_2]} vs {french_names[ai_1]}"


def final_rate_text(values):
    if not values:
        return "0.0%"
    return f"{values[-1]:.1f}%"


def plot_cumulative_win_rates(rows, results_dir: Path) -> None:
    plt = require_matplotlib()
    series = build_cumulative_score_rates(rows)
    colors = ["tab:orange", "crimson", "cornflowerblue"]
    linestyles = ["-", "--", "-."]
    markers = ["o", "s", "^"]

    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    ax.axhline(50, color="gray", linestyle="--", linewidth=1.2, alpha=0.7, label="50 %")

    for index, (color, pair_key) in enumerate(zip(colors, sorted(series.keys()))):
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

    if not match_results_path.exists():
        raise SystemExit(f"Missing match results file: {match_results_path}")

    rows = load_rows(match_results_path)
    plot_cumulative_win_rates(rows, results_dir)
    print(f"Wrote plot to {results_dir / 'difficulty_cumulative_blue_win_rate.png'}")


if __name__ == "__main__":
    main()