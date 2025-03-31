from utils import update_score

class GameTreeNode:
    def __init__(self, sequence, comp_score, human_score, is_comp_turn, move):
        self.sequence = sequence
        self.comp_score = comp_score
        self.human_score = human_score
        self.is_comp_turn = is_comp_turn
        self.move = move
        self.children = []

def build_game_tree(node, depth_limit):
    if depth_limit == 0 or not node.sequence:
        return

    for i in range(len(node.sequence)):
        new_sequence = node.sequence.copy()
        move = new_sequence.pop(i)
        
        # Fix: use node.is_comp_turn (instead of node.comp_turn)
        if node.is_comp_turn:
            new_comp_score, new_human_score = update_score(node.comp_score, node.human_score, move, True)
        else:
            temp_score, temp_opp = update_score(node.human_score, node.comp_score, move, True)
            new_human_score, new_comp_score = temp_score, temp_opp
        
        child = GameTreeNode(new_sequence, new_comp_score, new_human_score, not node.is_comp_turn, i)
        node.children.append(child)
        build_game_tree(child, depth_limit - 1)

def minimax(node, depth, maximizing):
    if depth == 0 or not node.sequence:
        return node.comp_score - node.human_score, None
    if not node.children:
        return node.comp_score - node.human_score, None

    if maximizing:
        max_eval = -float('inf')
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
    if depth == 0 or not node.sequence:
        return node.comp_score - node.human_score, None
    if not node.children:
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
                break
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
                break
        return min_eval, best_move
