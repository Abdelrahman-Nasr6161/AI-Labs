import math
from bfs import BFS
from puzzleState import PuzzleState

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
    print("3. IDS")
    print("4. A*")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ")
    
    if choice == '1':
        print("\nRunning BFS...")
        solution, trace = BFS(initial, goal)
        print(f"\nStates explored: {trace[-2]['explored_size'] if len(trace) > 1 else 0}")
        print_solution(solution)
        
    elif choice == '2':
        print("\nDFS not yet implemented")
        # solution, trace = dfs(initial, goal, trace=True)
        # print_solution(solution)
        
    elif choice == '3':
        print("\IDS not yet implemented")
        
    elif choice == '4':
        print("\nA* not yet implemented")
        
    elif choice == '5':
        print("\nExiting...")
    
    else:
        print("\nInvalid choice!")


if __name__ == "__main__":
    main()