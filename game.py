from game_processing import generate_sequence

class Game:
    def __init__(self, length, human_starts=True):
        self.sequence = generate_sequence(length)
        self.human_score = 50
        self.comp_score = 50
        self.is_comp_turn = not human_starts

    def make_move(self, index, is_human):
        number = self.sequence.pop(index)
        if number == 1:
            if is_human:
                self.human_score -= 1
            else:
                self.comp_score -= 1
        elif number == 2:
            self.human_score -= 1
            self.comp_score -= 1
        else:
            if is_human:
                self.comp_score -= 1
            else:
                self.human_score -= 1
        self.is_comp_turn = not is_human

    def is_game_over(self):
        return len(self.sequence) == 0

    def get_winner(self):
        if self.human_score > self.comp_score:
            return "Cilvēks uzvar!"
        elif self.comp_score > self.human_score:
            return "Dators uzvar!"
        else:
            return "Neizšķirts."
