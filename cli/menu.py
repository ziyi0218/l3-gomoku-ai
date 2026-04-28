from cli.input import ask_int
from experiments.depth_benchmark import benchmark_depths
from experiments.evaluation_benchmark import benchmark_evaluations
from modes.ai_vs_ai import play_ai_vs_ai
from modes.human_vs_ai import play_human_vs_ai


def main_menu() -> None:
    """Main menu."""
    while True:
        print("\n===================================")
        print("           Gomoku AI Menu")
        print("===================================")
        print("1. Human vs AI")
        print("2. AI vs AI")
        print("3. Depth benchmark")
        print("4. Evaluation benchmark")
        print("5. Quit")

        choice = ask_int("Choose mode: ", [1, 2, 3, 4, 5])

        if choice == 1:
            play_human_vs_ai()

        elif choice == 2:
            play_ai_vs_ai()

        elif choice == 3:
            benchmark_depths()

        elif choice == 4:
            benchmark_evaluations()

        elif choice == 5:
            print("Goodbye.")
            return
