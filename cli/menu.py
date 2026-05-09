from cli.input import ask_int
from modes.human_vs_ai import play_human_vs_ai
from modes.pvp import play_pvp


def main_menu() -> None:
    """Main menu."""
    while True:
        print("\n===================================")
        print("           Gomoku AI Menu")
        print("===================================")
        print("1. PvP - two human players")
        print("2. Human vs AI")
        print("3. Quit")

        choice = ask_int("Choose mode: ", [1, 2, 3])

        if choice == 1:
            play_pvp()

        elif choice == 2:
            play_human_vs_ai()

        elif choice == 3:
            print("Goodbye.")
            return
