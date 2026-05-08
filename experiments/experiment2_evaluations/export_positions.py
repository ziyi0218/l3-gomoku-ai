import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from experiments.experiment2_evaluations.positions import EVALUATION_POSITIONS

OUTPUT_PATH = Path("experiments/experiment2_evaluations/results/evaluation_positions.txt")

SYMBOLS = {
    0: ".",
    1: "X",
    -1: "O",
}


def render_board(board) -> str:
    header = "    " + " ".join(f"{c:2d}" for c in range(board.size))
    lines = [header]
    for r in range(board.size):
        cells = " ".join(f" {SYMBOLS[board.get(r, c)]}" for c in range(board.size))
        lines.append(f"{r:2d}  {cells}")
    return "\n".join(lines)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    sections = [
        "Experiment 2 Fixed Evaluation Positions",
        "X = black/current player in these positions, O = white, . = empty",
        "",
    ]

    for position in EVALUATION_POSITIONS:
        board = position.make_board()
        sections.extend(
            [
                "=" * 72,
                position.name,
                f"player_to_move: {position.player_to_move}",
                f"description: {position.description}",
                f"purpose: {position.purpose}",
                "moves:",
                ", ".join(f"({r},{c},{player})" for r, c, player in position.moves),
                "",
                render_board(board),
                "",
            ]
        )

    OUTPUT_PATH.write_text("\n".join(sections), encoding="utf-8")
    print(f"Wrote fixed positions to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
