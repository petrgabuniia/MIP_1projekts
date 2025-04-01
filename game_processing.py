import random

def update_score(player_score, opponent_score, move): # Punktu atjaunināšana
    if move == 1:
        player_score -= 1
    elif move == 2:
        player_score -= 1
        opponent_score -= 1
    elif move == 3:
        opponent_score -= 1
    return player_score, opponent_score


def generate_sequence(length):
    return [random.choice([1, 2, 3]) for _ in range(length)]

class GameTreeNode:
    def __init__(self, sequence, comp_score, human_score, is_comp_turn, move):
        self.sequence = sequence                # Pašreizējā skaitļu virkne
        self.comp_score = comp_score            # Datora punkti
        self.human_score = human_score          # Cilvēka punkti
        self.is_comp_turn = is_comp_turn        # Vai gājiens ir datoram
        self.move = move                        # Gājiens (indekss skaitļu virknē)
        self.children = []                      # Bērnu mezgli (turpmākie gājieni)

# Rekursīva spēles koku uzbūve līdz dziļuma ierobežojumam 
def build_game_tree(node, depth_limit):
    if depth_limit == 0 or not node.sequence:
        return
    for i in range(len(node.sequence)):
        new_sequence = node.sequence.copy()
        move = new_sequence.pop(i)

        # Punktu atjaunināšana
        if node.is_comp_turn:
            new_comp_score, new_human_score = update_score(node.comp_score, node.human_score, move)
        else:
            temp_score, temp_opp = update_score(node.human_score, node.comp_score, move)
            new_human_score, new_comp_score = temp_score, temp_opp

        # Bērnu mezglu izveide 
        child = GameTreeNode(new_sequence, new_comp_score, new_human_score, not node.is_comp_turn, i)
        node.children.append(child)

        # Rekursīvs izsaukums nākamajam līmenim
        build_game_tree(child, depth_limit - 1)

def minimax(node, depth, maximizing):
    if depth == 0 or not node.sequence:
        return node.comp_score - node.human_score, None

    if maximizing:
        max_eval = float('-inf')
        best_move = None
        for child in node.children:
            eval, _ = minimax(child, depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_move = child.move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for child in node.children:
            eval, _ = minimax(child, depth - 1, True)
            if eval < min_eval:
                min_eval = eval
                best_move = child.move
        return min_eval, best_move


def alphabeta(node, depth, alpha, beta, maximizing):
    if depth == 0 or not node.sequence or not node.children:
        return node.comp_score - node.human_score, None

    if maximizing:
        max_eval = -float('inf')
        best_move = None
        for child in node.children:
            eval, _ = alphabeta(child, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = child.move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Alfa nogriešana
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for child in node.children:
            eval, _ = alphabeta(child, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = child.move
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Beta nogriešana
        return min_eval, best_move


class AI:
    def __init__(self, algo_choice):
        self.algo_choice = algo_choice
    def choose_move(self, game):
        root = GameTreeNode(game.sequence.copy(), game.comp_score, game.human_score, game.is_comp_turn, None)
        build_game_tree(root, depth_limit = 30)
        if self.algo_choice == "1":
            score, move = minimax(root, 30, True)
        else:
            score, move = alphabeta(root, 30, -float('inf'), float('inf'), True)
        return move if move is not None else 0