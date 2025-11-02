import math
from bfs import BFS
from astar import astar, print_astar_solution
from puzzleState import PuzzleState
from dfs import DFS
from iddfs import IDDFS
import time
def parse_state(state_string, size=3):
    """
    Convert comma-separated string to 2D board.
    Args:
        state_string: e.g., "1,2,0,3,4,5,6,7,8"
        size: board dimension (3 for 3x3, 4 for 4x4, etc.)
    Returns:
        2D list representing the board
    """
    numbers = [int(x.strip()) for x in state_string.split(',')]
    
    # Validate input
    if len(numbers) != size * size:
        raise ValueError(f"Expected {size*size} numbers, got {len(numbers)}")
    
    # Convert to 2D board
    board = []
    for i in range(size):
        row = numbers[i * size:(i + 1) * size]
        board.append(row)
    
    return board

def print_solution(solution):
    """Pretty print the solution."""
    if solution:
        print(f"\nSolution found with {len(solution) - 1} moves:")
        print("="*50)
        for i, step in enumerate(solution):
            if step['move']:
                print(f"\nMove {i}: {step['move']}")
            else:
                print(f"\nStep {i}: Initial State")
            
            board_str = '\n'.join([' '.join(map(str, row)) for row in step['board']])
            print(board_str)
    else:
        print("\nNo solution found!")

def main():
    print("8-Puzzle Solver")
    print("="*50)
    
    # Get initial state from user
    print("\nEnter initial state as comma-separated numbers (0 for blank)")
    print("Example: 1,2,0,3,4,5,6,7,8")
    initial_input = input("Initial state: ").strip()
    
    goal_input = "0,1,2,3,4,5,6,7,8"
    
    # Parse inputs
    initial_board = parse_state(initial_input)
    goal_board = parse_state(goal_input)
    
    initial = PuzzleState(initial_board)
    goal = PuzzleState(goal_board)

    
    print("\nInitial State:")
    print(initial)
    print("\nGoal State:")
    print(goal)
    print("\n" + "="*50)
    
    # Menu
    print("\nSelect Search Algorithm:")
    print("1. BFS")
    print("2. DFS")
    print("3. IDDFS")
    print("4. A*")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ")
    
    if choice == '1':
        print("\nRunning BFS...")
        start = time.time()
        solution, trace,expanded,depth = BFS(initial, goal)
        end = time.time()
        time_elapsed = end - start
        print(f"\nStates explored: {trace[-2]['explored_size'] if len(trace) > 1 else 0}")
        print_solution(solution)
        print(f"Execution Time : {time_elapsed}")
        print(f'Max Depth : {depth}')
        with open('bfs.txt','w') as F:
            for matrix in expanded:
                for row in matrix:
                    for element in row:
                        F.write(f"{str(element)} ")
                    F.write("\n")
                F.write("\n")
        
    elif choice == '2':
        print("\nRunning DFS...")
        start = time.time()
        solution, trace,expanded,depth = DFS(initial, goal)
        end = time.time()
        time_elapsed = end - start
        print(f"\nStates explored: {trace[-2]['explored_size'] if len(trace) > 1 else 0}")
        print_solution(solution)
        print(f"Execution Time : {time_elapsed}")
        print(f'Max Depth : {depth}')
        with open('dfs.txt','w') as F:
            for matrix in expanded:
                for row in matrix:
                    for element in row:
                        F.write(f"{str(element)} ")
                    F.write("\n")
                F.write("\n")

        
        
    elif choice == '3':
        print("\nRunning IDDFS...")
        start = time.time()
        solution, trace,expanded,depth = IDDFS(initial, goal)
        end = time.time()
        time_elapsed = end - start
        print(f"\nStates explored: {trace[-2]['explored_size'] if len(trace) > 1 else 0}")
        print_solution(solution)
        print(f"Execution Time : {time_elapsed}")
        print(f'Max Depth : {depth}')
        with open('iddfs.txt','w') as F:
            for matrix in expanded:
                for row in matrix:
                    for element in row:
                        F.write(f"{str(element)} ")
                    F.write("\n")
                F.write("\n")
        
    elif choice == '4':
        # heuristic = input("Choose heuristic (manhattan/euclidean): ")
        while True:
            heur_choice = input("Choose heuristic (manhattan/euclidean): ").strip().lower()
            if heur_choice in ('manhattan', 'euclidean'):
                break
            print("Invalid choice. Please enter 'manhattan' or 'euclidean'.")
        start = time.time()
        solution, trace, expanded_nodes, max_depth, heuristic_name = astar(initial, goal, heur_choice)
        end = time.time()
        time_elapsed = end-start
        print_astar_solution(solution, trace, heuristic_name)
        print(f"Execution Time : {time_elapsed}")
        print(f'Max Depth : {max_depth}')
        with open(f'a*{heuristic_name}.txt','w') as F:
            for matrix in expanded_nodes:
                for row in matrix:
                    for element in row:
                        F.write(f"{str(element)} ")
                    F.write("\n")
                F.write("\n")

        
        
    elif choice == '5':
        print("\nExiting...")
    
    else:
        print("\nInvalid choice!")

if __name__ == "__main__":
    main()