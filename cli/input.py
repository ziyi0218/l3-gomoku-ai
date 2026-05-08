from typing import List, Optional, Tuple

from ai.evaluation import eval_advanced, eval_basic, eval_intermediate
from ai.player import SEARCH_ALPHABETA
from models import EvalFn

AI_DIFFICULTIES = {
    1: ("Easy", 1, eval_basic, "Eval A", SEARCH_ALPHABETA),
    2: ("Medium", 3, eval_basic, "Eval A", SEARCH_ALPHABETA),
    3: ("Hard", 2, eval_intermediate, "Eval B", SEARCH_ALPHABETA),
}


def parse_move(s: str) -> Optional[Tuple[int, int] | tuple[str, str]]:
    """Parse human input."""
    s = s.strip().lower()

    if s in ("q", "quit", "exit"):
        return None

    if s in ("u", "undo"):
        return ("UNDO", "UNDO")

    s = s.replace("，", ",").replace(" ", ",")
    parts = [p for p in s.split(",") if p]

    if len(parts) != 2:
        return None

    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None


def ask_int(prompt: str, valid_values: List[int]) -> int:
    """Ask user for an integer from valid values."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value in valid_values:
                return value
            print(f"Please choose one of: {valid_values}")
        except ValueError:
            print("Please enter a valid number.")


def ask_depth() -> int:
    """Ask user to choose one search depth."""
    print("\nChoose AI search depth / profondeur:")
    print("1. Depth 1")
    print("2. Depth 2")
    print("3. Depth 3")

    return ask_int("Your choice: ", [1, 2, 3])


def ask_depth_list() -> List[int]:
    """
    Ask user which depths to benchmark.

    Example:
        1 2
        1 2 3
    """
    while True:
        raw = input(
            "\nWhich depths do you want to test? "
            "Enter values like '1 2' or '1 2 3': "
        ).strip()

        parts = raw.replace(",", " ").split()

        try:
            depths = sorted(set(int(x) for x in parts))
        except ValueError:
            print("Please enter numbers only, for example: 1 2 3")
            continue

        if len(depths) < 2:
            print("Please choose at least two depths.")
            continue

        if any(d not in [1, 2, 3] for d in depths):
            print("Allowed depths are only 1, 2, and 3.")
            continue

        return depths


def ask_positive_int(prompt: str) -> int:
    """Ask user for any positive integer."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value > 0:
                return value
            print("Please enter a positive integer.")
        except ValueError:
            print("Please enter a valid number.")


def ask_evaluation() -> Tuple[EvalFn, str]:
    """Ask user to choose an evaluation function."""
    print("\nChoose evaluation function:")
    print("1. Eval A - consecutive segment length")
    print("2. Eval B - segment length + open ends")
    print("3. Eval C - five-cell window potential")

    choice = ask_int("Your choice: ", [1, 2, 3])

    if choice == 1:
        return eval_basic, "Eval A"
    if choice == 2:
        return eval_intermediate, "Eval B"
    return eval_advanced, "Eval C"


def ask_ai_difficulty() -> Tuple[str, int, EvalFn, str, str]:
    """Ask user to choose one fixed AI difficulty profile."""
    print("\nChoose AI difficulty:")
    print("1. Easy   - A1 (Eval A, depth 1)")
    print("2. Medium - A3 (Eval A, depth 3)")
    print("3. Hard   - B2 (Eval B, depth 2)")

    choice = ask_int("Your choice: ", [1, 2, 3])
    return AI_DIFFICULTIES[choice]


def ask_search_algorithm() -> str:
    """Ask user to choose a search algorithm."""
    print("\nChoose search algorithm:")
    print("1. Minimax")
    print("2. Alpha-Beta pruning")

    choice = ask_int("Your choice: ", [1, 2])

    if choice == 1:
        return SEARCH_MINIMAX
    return SEARCH_ALPHABETA
