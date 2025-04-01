import time
from game_processing import GameTreeNode, build_game_tree, minimax, alphabeta

def run_test(sequence, depth_limit, is_comp_turn=True, comp_score=50, human_score=50):
    
    root = GameTreeNode(sequence.copy(), comp_score, human_score, is_comp_turn, None)
    
    build_game_tree(root, depth_limit)
    
    start_time = time.time()
    minimax_result, minimax_move = minimax(root, depth_limit, True)
    minimax_time = time.time() - start_time

    start_time = time.time()
    alphabeta_result, alphabeta_move = alphabeta(root, depth_limit, -float('inf'), float('inf'), True)
    alphabeta_time = time.time() - start_time

    return {
        "minimax_result": minimax_result,
        "minimax_move": minimax_move,
        "minimax_time": minimax_time,
        "alphabeta_result": alphabeta_result,
        "alphabeta_move": alphabeta_move,
        "alphabeta_time": alphabeta_time
    }

def main():
    sequences = [
        [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
        [2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1],
        [3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2]
    ]
    depth_limit = 6

    for i, seq in enumerate(sequences, start=1):
        print(f"Test case {i}: Sequence = {seq}")
        results = run_test(seq, depth_limit)
        print("Minimax:    Result =", results["minimax_result"],
              "Move =", results["minimax_move"],
              "Time = {:.6f} seconds".format(results["minimax_time"]))
        print("Alpha-Beta: Result =", results["alphabeta_result"],
              "Move =", results["alphabeta_move"],
              "Time = {:.6f} seconds".format(results["alphabeta_time"]))
        print("-" * 50)

if __name__ == '__main__':
    main()
