import random

def generate_sequence(length):
    return [random.randint(1, 3) for _ in range(length)]

def update_score(player_score, opponent_score, number_removed, is_player_turn):
    if number_removed == 1:
        if is_player_turn:
            player_score -= 1
        else:
            opponent_score -= 1
    elif number_removed == 2:
        player_score -= 1
        opponent_score -= 1
    else:
        if is_player_turn:
            opponent_score -= 1
        else:
            player_score -= 1

    return player_score, opponent_score