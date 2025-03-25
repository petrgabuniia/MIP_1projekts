from game import Game
from player import HumanPlayer, ComputerPlayer
from utils import update_score
from game_tree import GameTreeNode, build_game_tree
import random

class AI:
    def choose_move(self, game: Game):
        for i, num in enumerate(game.sequence):
            if num == 3:
                return i
        for i, num in enumerate(game.sequence):
            if num == 2:
                return i
        return 0

def run_game():
    while True:
        try:
            length = int(input("Ievadiet skaitļu virknes garumu (15-25): "))
            if 15 <= length <= 25:
                break
            else:
                print("Garumam jābūt no 15 līdz 25.")
        except ValueError:
            print("Ievadiet skaitli!")

    game = Game(length)
    ai = AI()

    print(f"\nSpēles sākums. Virkne: {game.sequence}")
    print(f"Cilvēks: 50 punkti, Dators: 50 punkti")

    while not game.is_game_over():
        print(f"\nAtlikusī virkne: {game.sequence}")
        print(f"Punkti — Cilvēks: {game.human_score}, Dators: {game.comp_score}")

        if not game.is_comp_turn:
            while True:
                try:
                    number = int(input("Ievadiet skaitli (1, 2 vai 3): "))
                    if number in [1, 2, 3] and number in game.sequence:
                        index = game.sequence.index(number)
                        break
                    else:
                        print(f"Skaitlis {number} nav atlikušajā virknē!")
                except ValueError:
                    print("Ievadiet skaitli!")
            game.make_move(index, is_human=True)
            game.is_comp_turn = True

        else:
            index = ai.choose_move(game)
            print(f"Dators izvēlas indeksu {index} (vērtība {game.sequence[index]})")
            game.make_move(index, is_human=False)
            game.is_comp_turn = False

    print(f"\nSpēle beigusies.")
    print(f"Rezultāts — Cilvēks: {game.human_score}, Dators: {game.comp_score}")
    print(game.get_winner())

if __name__ == '__main__':
    run_game()