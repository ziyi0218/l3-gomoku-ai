import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from experiments.experiment2_evaluations.positions import EVALUATION_POSITIONS
from game.rules import generate_candidate_moves, get_winner, is_terminal
from game.utils import format_board

OUTPUT_PATH = Path("experiments/experiment2_evaluations/results/evaluation_positions.txt")


def player_text(player: int) -> str:
    if player == 1:
        return "Black / X"
    return "White / O"


def winner_text(winner) -> str:
    if winner == 1:
        return "Black / X"
    if winner == -1:
        return "White / O"
    return "None"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    sections = []

    for position in EVALUATION_POSITIONS:
        board = position.make_board()
        candidates = generate_candidate_moves(board, radius=2)
        winner = get_winner(board)
        sections.append(
            "\n".join(
                [
                    "=" * 80,
                    position.name,
                    "=" * 80,
                    f"Description: {position.description}",
                    f"Purpose: {position.purpose}",
                    f"Player to move: {player_text(position.player_to_move)}",
                    f"Stones: {len(board.stones)}",
                    f"Candidate rule: generate_candidate_moves(radius=2)",
                    f"Candidate count: {len(candidates)}",
                    f"Terminal: {is_terminal(board)}",
                    f"Winner: {winner_text(winner)}",
                    "",
                    format_board(board),
                    "",
                ]
            )
        )

    OUTPUT_PATH.write_text("\n".join(sections), encoding="utf-8")
    print(f"Wrote evaluation position boards to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
