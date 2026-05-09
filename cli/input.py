from dataclasses import dataclass
from typing import List, Optional, Tuple

from ai.evaluation import eval_advanced, eval_basic, eval_intermediate
from ai.player import SEARCH_ALPHABETA
from models import EvalFn


@dataclass(frozen=True)
class DifficultyProfile:
    name: str
    label: str
    depth: int
    eval_fn: EvalFn
    eval_name: str
    search_name: str
    use_ordering: bool
    candidate_radius: int


AI_DIFFICULTIES = {
    1: DifficultyProfile("Easy", "A1", 1, eval_basic, "Eval A", SEARCH_ALPHABETA, False, 2),
    2: DifficultyProfile("Medium", "A3", 3, eval_basic, "Eval A", SEARCH_ALPHABETA, True, 2),
    3: DifficultyProfile("Hard", "B2", 2, eval_intermediate, "Eval B", SEARCH_ALPHABETA, True, 3),
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


def ask_ai_difficulty() -> DifficultyProfile:
    """Ask user to choose one fixed AI difficulty profile."""
    print("\nChoose AI difficulty:")
    print("1. Easy   - A1 (Eval A, depth 1, Alpha-Beta, ordering off, radius 2)")
    print("2. Medium - A3 (Eval A, depth 3, Alpha-Beta + ordering, radius 2)")
    print("3. Hard   - B2 (Eval B, depth 2, Alpha-Beta + ordering, radius 3)")
    print("4. Custom - manual eval/depth/radius, Alpha-Beta + ordering")

    choice = ask_int("Your choice: ", [1, 2, 3, 4])
    if choice in AI_DIFFICULTIES:
        return AI_DIFFICULTIES[choice]

    return ask_custom_ai_profile()


def ask_custom_ai_profile() -> DifficultyProfile:
    """Ask user to configure one AI profile with fixed Alpha-Beta ordering."""
    print("\nCustom AI configuration")
    print("Search is fixed: Alpha-Beta + ordering")

    print("\nChoose evaluation:")
    print("1. Eval A - basic defensive consecutive-segment evaluation")
    print("2. Eval B - open / blocked shape evaluation")
    print("3. Eval C - five-cell window potential evaluation")
    eval_choice = ask_int("Evaluation: ", [1, 2, 3])

    if eval_choice == 1:
        eval_fn = eval_basic
        eval_name = "Eval A"
    elif eval_choice == 2:
        eval_fn = eval_intermediate
        eval_name = "Eval B"
    else:
        eval_fn = eval_advanced
        eval_name = "Eval C"

    print("\nChoose search depth:")
    print("1. Depth 1")
    print("2. Depth 2")
    print("3. Depth 3")
    depth = ask_int("Depth: ", [1, 2, 3])

    print("\nChoose candidate radius:")
    print("1. Radius 1 - fastest, narrowest")
    print("2. Radius 2 - standard")
    print("3. Radius 3 - wider, slower")
    candidate_radius = ask_int("Radius: ", [1, 2, 3])

    label = f"Custom {eval_name} D{depth} R{candidate_radius}"
    return DifficultyProfile(
        name="Custom",
        label=label,
        depth=depth,
        eval_fn=eval_fn,
        eval_name=eval_name,
        search_name=SEARCH_ALPHABETA,
        use_ordering=True,
        candidate_radius=candidate_radius,
    )
