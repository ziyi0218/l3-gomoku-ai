import argparse
import csv
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Dict, List

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai.alphabeta import choose_move_alphabeta
from experiments.experiment4_difficulty_tournament.openings import (
    OPENING_POSITIONS,
    OpeningPosition,
)
from experiments.experiment4_difficulty_tournament.profiles import (
    AIProfile,
    DIFFICULTY_AI_PROFILES,
)
from game.board import Board
from game.rules import get_winner, is_terminal

RESULT_DIR = Path("experiments/experiment4_difficulty_tournament/result7")
MATCH_RESULTS_CSV = RESULT_DIR / "difficulty_match_results.csv"
RANKING_CSV = RESULT_DIR / "difficulty_ai_ranking.csv"
PAIRWISE_CSV = RESULT_DIR / "difficulty_pairwise_summary.csv"
RANKING_MD = RESULT_DIR / "difficulty_ai_ranking.md"


@dataclass
class GameResult:
    game_id: int
    pair_id: str
    opening_name: str
    black_ai: str
    white_ai: str
    winner: str
    winner_ai: str
    result_for_black: str
    moves_count: int
    black_total_time_ms: float
    white_total_time_ms: float
    black_avg_time_ms: float
    white_avg_time_ms: float
    black_total_nodes: int
    white_total_nodes: int
    black_avg_nodes: float
    white_avg_nodes: float
    max_moves_reached: bool


def choose_ai_move(board: Board, player: int, profile: AIProfile):
    move, _, stats = choose_move_alphabeta(
        board=board,
        player=player,
        depth=profile.depth,
        eval_fn=profile.eval_fn,
        use_ordering=profile.use_ordering,
        candidate_radius=profile.candidate_radius,
    )
    return move, stats


def play_ai_vs_ai(
    black_ai: AIProfile,
    white_ai: AIProfile,
    game_id: int,
    pair_id: str,
    max_moves: int,
    opening: OpeningPosition,
) -> GameResult:
    board = opening.make_board()
    current = opening.player_to_move

    if current not in (1, -1):
        raise ValueError(f"Invalid player_to_move for opening {opening.name}: {current}")

    black_total_time = 0.0
    white_total_time = 0.0
    black_total_nodes = 0
    white_total_nodes = 0
    black_moves = 0
    white_moves = 0

    moves_count = 0
    max_moves_reached = False

    while moves_count < max_moves:
        profile = black_ai if current == 1 else white_ai
        move, stats = choose_ai_move(board, current, profile)

        if move is None:
            max_moves_reached = True
            break

        placed = board.place(move[0], move[1], current)
        if not placed:
            raise RuntimeError(f"Illegal move selected by {profile.name}: {move}")

        moves_count += 1

        if current == 1:
            black_moves += 1
            black_total_time += stats.time_ms
            black_total_nodes += stats.nodes
        else:
            white_moves += 1
            white_total_time += stats.time_ms
            white_total_nodes += stats.nodes

        if is_terminal(board):
            break

        current = -current

    if moves_count >= max_moves and not is_terminal(board):
        max_moves_reached = True

    winner_value = get_winner(board)
    if winner_value == 1:
        winner = "black"
        winner_ai = black_ai.name
        result_for_black = "win"
    elif winner_value == -1:
        winner = "white"
        winner_ai = white_ai.name
        result_for_black = "loss"
    else:
        winner = "draw"
        winner_ai = ""
        result_for_black = "draw"

    return GameResult(
        game_id=game_id,
        pair_id=pair_id,
        opening_name=opening.name,
        black_ai=black_ai.name,
        white_ai=white_ai.name,
        winner=winner,
        winner_ai=winner_ai,
        result_for_black=result_for_black,
        moves_count=moves_count,
        black_total_time_ms=round(black_total_time, 4),
        white_total_time_ms=round(white_total_time, 4),
        black_avg_time_ms=round(black_total_time / black_moves, 4) if black_moves else 0.0,
        white_avg_time_ms=round(white_total_time / white_moves, 4) if white_moves else 0.0,
        black_total_nodes=black_total_nodes,
        white_total_nodes=white_total_nodes,
        black_avg_nodes=round(black_total_nodes / black_moves, 2) if black_moves else 0.0,
        white_avg_nodes=round(white_total_nodes / white_moves, 2) if white_moves else 0.0,
        max_moves_reached=max_moves_reached,
    )


def build_game_jobs(games_per_pair: int, max_moves: int):
    if games_per_pair <= 0:
        raise ValueError("games_per_pair must be positive")
    if games_per_pair % 2 != 0:
        raise ValueError("games_per_pair must be even so first player is balanced")

    jobs = []
    game_id = 1

    for ai_1, ai_2 in combinations(DIFFICULTY_AI_PROFILES, 2):
        pair_id = f"{ai_1.name}_vs_{ai_2.name}"
        games_each_side = games_per_pair // 2

        for index in range(games_each_side):
            opening = OPENING_POSITIONS[index % len(OPENING_POSITIONS)]
            jobs.append((ai_1, ai_2, game_id, pair_id, max_moves, opening))
            game_id += 1

        for index in range(games_each_side):
            opening = OPENING_POSITIONS[index % len(OPENING_POSITIONS)]
            jobs.append((ai_2, ai_1, game_id, pair_id, max_moves, opening))
            game_id += 1

    return jobs


def run_game_job(job) -> GameResult:
    black_ai, white_ai, game_id, pair_id, max_moves, opening = job
    return play_ai_vs_ai(black_ai, white_ai, game_id, pair_id, max_moves, opening)


def run_round_robin(games_per_pair: int, max_moves: int) -> List[GameResult]:
    jobs = build_game_jobs(games_per_pair, max_moves)
    results: List[GameResult] = []
    total_games = len(jobs)

    for job in jobs:
        black_ai, white_ai, game_id, _, _, opening = job
        print(
            f"Game {game_id}/{total_games}: {black_ai.name} black vs {white_ai.name} white"
            f" on {opening.name}"
        )
        results.append(run_game_job(job))

    return results


def run_round_robin_parallel(
    games_per_pair: int,
    max_moves: int,
    workers: int,
) -> List[GameResult]:
    jobs = build_game_jobs(games_per_pair, max_moves)
    total_games = len(jobs)
    results: List[GameResult] = []

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(run_game_job, job): job for job in jobs}
        completed = 0

        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            completed += 1
            print(
                f"Completed {completed}/{total_games}: "
                f"game {result.game_id} {result.black_ai} vs {result.white_ai}"
            )

    results.sort(key=lambda result: result.game_id)
    return results


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("No rows to write")

    with path.open("w", newline="", encoding="utf-8") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def game_rows(results: List[GameResult]) -> List[Dict[str, object]]:
    return [result.__dict__ for result in results]


def build_ranking_rows(results: List[GameResult]) -> List[Dict[str, object]]:
    stats = {
        profile.name: {
            "ai": profile.name,
            "profile": profile.label,
            "evaluation": profile.evaluation_name,
            "depth": profile.depth,
            "games": 0,
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "games_as_black": 0,
            "wins_as_black": 0,
            "games_as_white": 0,
            "wins_as_white": 0,
            "total_time": 0.0,
            "total_nodes": 0,
            "total_moves": 0,
            "total_game_length": 0,
        }
        for profile in DIFFICULTY_AI_PROFILES
    }

    for result in results:
        update_ai_stats(stats[result.black_ai], result, is_black=True)
        update_ai_stats(stats[result.white_ai], result, is_black=False)

    rows = []
    for item in stats.values():
        games = item["games"]
        non_draw_games = item["wins"] + item["losses"]
        total_moves = item["total_moves"]
        games_as_black = item["games_as_black"]
        games_as_white = item["games_as_white"]

        rows.append(
            {
                "ai": item["ai"],
                "profile": item["profile"],
                "evaluation": item["evaluation"],
                "depth": item["depth"],
                "games": games,
                "wins": item["wins"],
                "losses": item["losses"],
                "draws": item["draws"],
                "win_rate": round(item["wins"] / games, 4) if games else 0.0,
                "score_rate": round((item["wins"] + 0.5 * item["draws"]) / games, 4) if games else 0.0,
                "non_draw_win_rate": round(item["wins"] / non_draw_games, 4) if non_draw_games else 0.0,
                "avg_time_per_move_ms": round(item["total_time"] / total_moves, 4) if total_moves else 0.0,
                "avg_nodes_per_move": round(item["total_nodes"] / total_moves, 2) if total_moves else 0.0,
                "games_as_black": games_as_black,
                "wins_as_black": item["wins_as_black"],
                "black_win_rate": round(item["wins_as_black"] / games_as_black, 4) if games_as_black else 0.0,
                "games_as_white": games_as_white,
                "wins_as_white": item["wins_as_white"],
                "white_win_rate": round(item["wins_as_white"] / games_as_white, 4) if games_as_white else 0.0,
                "avg_game_length": round(item["total_game_length"] / games, 2) if games else 0.0,
            }
        )

    rows.sort(
        key=lambda row: (
            -float(row["score_rate"]),
            -float(row["win_rate"]),
            float(row["avg_time_per_move_ms"]),
            float(row["avg_nodes_per_move"]),
            row["ai"],
        )
    )
    return rows


def update_ai_stats(item: Dict[str, object], result: GameResult, is_black: bool) -> None:
    item["games"] += 1
    item["total_game_length"] += result.moves_count

    if is_black:
        item["games_as_black"] += 1
        item["total_time"] += result.black_total_time_ms
        item["total_nodes"] += result.black_total_nodes
        item["total_moves"] += (result.moves_count + 1) // 2
        if result.winner == "black":
            item["wins"] += 1
            item["wins_as_black"] += 1
        elif result.winner == "white":
            item["losses"] += 1
        else:
            item["draws"] += 1
    else:
        item["games_as_white"] += 1
        item["total_time"] += result.white_total_time_ms
        item["total_nodes"] += result.white_total_nodes
        item["total_moves"] += result.moves_count // 2
        if result.winner == "white":
            item["wins"] += 1
            item["wins_as_white"] += 1
        elif result.winner == "black":
            item["losses"] += 1
        else:
            item["draws"] += 1


def build_pairwise_rows(results: List[GameResult]) -> List[Dict[str, object]]:
    grouped = defaultdict(list)
    for result in results:
        ai_1, _, ai_2 = result.pair_id.partition("_vs_")
        grouped[(ai_1, ai_2)].append(result)

    rows = []
    for (ai_1, ai_2), games in sorted(grouped.items()):
        ai_1_wins = sum(1 for game in games if game.winner_ai == ai_1)
        ai_2_wins = sum(1 for game in games if game.winner_ai == ai_2)
        draws = sum(1 for game in games if game.winner == "draw")
        ai_1_time, ai_1_moves = total_time_and_moves_for_ai(games, ai_1)
        ai_2_time, ai_2_moves = total_time_and_moves_for_ai(games, ai_2)

        rows.append(
            {
                "ai_1": ai_1,
                "ai_2": ai_2,
                "games": len(games),
                "ai_1_wins": ai_1_wins,
                "ai_2_wins": ai_2_wins,
                "draws": draws,
                "ai_1_win_rate": round(ai_1_wins / len(games), 4),
                "ai_2_win_rate": round(ai_2_wins / len(games), 4),
                "ai_1_score_rate": round((ai_1_wins + 0.5 * draws) / len(games), 4),
                "ai_2_score_rate": round((ai_2_wins + 0.5 * draws) / len(games), 4),
                "avg_moves": round(sum(game.moves_count for game in games) / len(games), 2),
                "avg_time_per_move_ai_1": round(ai_1_time / ai_1_moves, 4) if ai_1_moves else 0.0,
                "avg_time_per_move_ai_2": round(ai_2_time / ai_2_moves, 4) if ai_2_moves else 0.0,
            }
        )

    return rows


def total_time_and_moves_for_ai(games: List[GameResult], ai_name: str):
    total_time = 0.0
    total_moves = 0
    for game in games:
        if game.black_ai == ai_name:
            total_time += game.black_total_time_ms
            total_moves += (game.moves_count + 1) // 2
        elif game.white_ai == ai_name:
            total_time += game.white_total_time_ms
            total_moves += game.moves_count // 2
    return total_time, total_moves


def write_ranking_markdown(path: Path, ranking_rows: List[Dict[str, object]]) -> None:
    headers = [
        "ai",
        "profile",
        "evaluation",
        "depth",
        "games",
        "wins",
        "losses",
        "draws",
        "win_rate",
        "score_rate",
        "avg_time_per_move_ms",
        "avg_nodes_per_move",
        "black_win_rate",
        "white_win_rate",
    ]
    lines = [
        "# Experiment 4 Difficulty AI Ranking",
        "",
        "|" + "|".join(headers) + "|",
        "|" + "|".join(["---"] * len(headers)) + "|",
    ]
    for row in ranking_rows:
        lines.append("|" + "|".join(str(row[h]) for h in headers) + "|")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Experiment 4: final Easy/Medium/Hard AI tournament."
    )
    parser.add_argument("--games-per-pair", type=int, default=200)
    parser.add_argument("--max-moves", type=int, default=50)
    parser.add_argument("--output-dir", type=Path, default=RESULT_DIR)
    parser.add_argument("--workers", type=int, default=4)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.workers > 1:
        results = run_round_robin_parallel(args.games_per_pair, args.max_moves, args.workers)
    else:
        results = run_round_robin(args.games_per_pair, args.max_moves)

    match_path = output_dir / MATCH_RESULTS_CSV.name
    ranking_path = output_dir / RANKING_CSV.name
    pairwise_path = output_dir / PAIRWISE_CSV.name
    ranking_md_path = output_dir / RANKING_MD.name

    write_csv(match_path, game_rows(results))
    ranking_rows = build_ranking_rows(results)
    write_csv(ranking_path, ranking_rows)
    write_ranking_markdown(ranking_md_path, ranking_rows)
    write_csv(pairwise_path, build_pairwise_rows(results))

    print(f"Wrote raw match results: {match_path}")
    print(f"Wrote AI ranking: {ranking_path}")
    print(f"Wrote pairwise summary: {pairwise_path}")
    print(f"Wrote ranking markdown: {ranking_md_path}")


if __name__ == "__main__":
    main()