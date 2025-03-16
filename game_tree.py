from utils import update_scores

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
        
        if node.comp_turn:
            new_comp_score, new_human_score = update_scores(node.comp_score, node.human_score, move, True)
        else:
            temp_score, temp_opp = update_scores(node.human_score, node.comp_score, move, True)
            new_human_score, new_comp_score = temp_score, temp_opp
        
        child = GameTreeNode(new_sequence, new_comp_score, new_human_score, not node.comp_turn, i)
        node.children.append(child)
        build_game_tree(child, depth_limit - 1)