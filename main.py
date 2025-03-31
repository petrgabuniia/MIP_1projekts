from game import Game
from utils import update_score
from game_tree import GameTreeNode, build_game_tree, minimax, alphabeta


class AI:
    def __init__(self, algorithm_choice):
        self.algorithm = algorithm_choice

    def choose_move(self, game: Game):
        depth_limit = 4  
        root = GameTreeNode(game.sequence.copy(), game.comp_score, game.human_score, game.is_comp_turn, None)
        build_game_tree(root, depth_limit)
        if self.algorithm == '1':
            _, best_move = minimax(root, depth_limit, True)
        else:
            _, best_move = alphabeta(root, depth_limit, -float('inf'), float('inf'), True)
        if best_move is None:
            for i, num in enumerate(game.sequence):
                if num == 3:
                    return i
            for i, num in enumerate(game.sequence):
                if num == 2:
                    return i
            return 0
        return best_move

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
    

    while True:
        algo_choice = input("Izvēlieties datoralgoritmu (1 - minimax, 2 - alpha-beta): ")
        if algo_choice in ['1', '2']:
            break
        else:
            print("Nepareiza izvēle, mēģiniet vēlreiz.")

    game = Game(length)
    ai = AI(algo_choice)

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
