import time
import tracemalloc
from game_processing import GameTreeNode, build_game_tree, minimax, alphabeta

def run_test(sequence, depth_limit, is_comp_turn=True, comp_score=50, human_score=50):
    
    root = GameTreeNode(sequence.copy(), comp_score, human_score, is_comp_turn, None)
    
    build_game_tree(root, depth_limit)
    
    start_time = time.time()
    minimax_result, minimax_move = minimax(root, depth_limit, True)
    minimax_time = time.time() - start_time
    start_time = time.time()

    tracemalloc.start()
    minimax_result, minimax_move = minimax(root, depth_limit, True)
    _, minimax_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    alphabeta_result, alphabeta_move = alphabeta(root, depth_limit, -float('inf'), float('inf'), True)
    alphabeta_time = time.time() - start_time

    tracemalloc.start()
    alphabeta_result, alphabeta_move = alphabeta(root, depth_limit, -float('inf'), float('inf'), True)
    _, alphabeta_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "minimax_memory": minimax_peak,
        "alphabeta_memory": alphabeta_peak,
        "minimax_time": minimax_time,
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
        print(f"Minimax Peak Memory: {results['minimax_memory']} bytes")
        print(f"Alpha-Beta Peak Memory: {results['alphabeta_memory']} bytes")
        print(f"Minimax Time: {results['minimax_time']} seconds")
        print(f"Alpha-Beta Time: {results['alphabeta_time']} seconds")
        print("-" * 50)

if __name__ == '__main__':
    main()
