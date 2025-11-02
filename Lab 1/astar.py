import heapq
import copy
from puzzleState import PuzzleState, reconstruct_path
import math

def manhattan_distance(board, goal_board):
    """
    Manhattan distance heuristic = Sum of absolute differences in x and y coordinates.
    """
    distance = 0
    size = len(board)
    
    # Create a mapping of values to goal positions
    goal_positions = {}
    for i in range(size):
        for j in range(size):
            goal_positions[goal_board[i][j]] = (i, j)
    
    # Calculate Manhattan distance for each tile (except blank/0)
    for i in range(size):
        for j in range(size):
            value = board[i][j]
            if value != 0:  # Skip blank tile
                goal_i, goal_j = goal_positions[value]
                distance += abs(i - goal_i) + abs(j - goal_j)
    
    return distance

def euclidean_distance(board, goal_board):
    """
    Calculate Euclidean distance heuristic = Straight-line distance between current and goal positions.
    """
    distance = 0.0
    size = len(board)
    
    # Create a mapping of values to goal positions
    goal_positions = {}
    for i in range(size):
        for j in range(size):
            goal_positions[goal_board[i][j]] = (i, j)
    
    # Calculate Euclidean distance for each tile (except blank/0)
    for i in range(size):
        for j in range(size):
            value = board[i][j]
            if value != 0:  # Skip blank tile
                goal_i, goal_j = goal_positions[value]
                distance += math.sqrt((i - goal_i)**2 + (j - goal_j)**2)
    
    return distance


class AStarNode:
    """Node for A* search with f(n) = g(n) + h(n)"""
    def __init__(self, state, g_cost, h_cost):
        self.state = state
        self.g_cost = g_cost  # Cost from start to current node
        self.h_cost = h_cost  # Heuristic cost to goal
        self.f_cost = g_cost + h_cost  # Total cost
    
    def __lt__(self, other):
        # For heap comparison - lower f_cost has higher priority
        return self.f_cost < other.f_cost
    
    def __eq__(self, other):
        return self.f_cost == other.f_cost


def calculate_true_distance(state, goal_state):
    """
    Calculate the true minimum distance (optimal solution length) from state to goal.
    Uses BFS to find the shortest path.
    """
    from collections import deque
    
    if state == goal_state:
        return 0
    
    frontier = deque([(state, 0)])
    explored = {state.to_tuple()}
    
    while frontier:
        current, depth = frontier.popleft()
        
        for neighbor in current.get_neighbors():
            neighbor_tuple = neighbor.to_tuple()
            
            if neighbor_tuple not in explored:
                if neighbor == goal_state:
                    return depth + 1
                
                explored.add(neighbor_tuple)
                frontier.append((neighbor, depth + 1))
    
    return float('inf')  # No path exists

def astar(initial_state, goal_state, heuristic='manhattan', trace=True):
    """
    Perform A* search on the 8-puzzle problem with state-hashing.

    Args:
        initial_state: PuzzleState object representing the start
        goal_state: PuzzleState object representing the goal
        heuristic: 'manhattan' or 'euclidean'
        trace: Include detailed intermediate logs if True

    Returns:
        (solution_path, trace_data, expanded_nodes, max_depth, heuristic_name)
    """
    # Choose heuristic
    heuristic_func = manhattan_distance if heuristic == 'manhattan' else euclidean_distance
    heuristic_name = "Manhattan Distance" if heuristic == 'manhattan' else "Euclidean Distance"

    # Initial setup
    h_initial = heuristic_func(initial_state.board, goal_state.board)
    initial_node = AStarNode(initial_state, 0, h_initial)
    frontier = [initial_node]
    frontier_dict = {initial_state.to_tuple(): initial_node}
    heapq.heapify(frontier)

    explored = set()  # {state_tuple}
    trace_data = []
    expanded_nodes = []
    max_depth = 0
    step = 0

    if trace:
        trace_data.append({
            'step': 0,
            'action': 'initialize',
            'current_state': copy.deepcopy(initial_state.board),
            'message': f'Starting A* with {heuristic_name}',
            'g_cost': 0, 'h_cost': h_initial, 'f_cost': h_initial,
            'frontier_size': 1, 'explored_size': 0
        })

    while frontier:
        step += 1
        current_node = heapq.heappop(frontier)
        state = current_node.state
        state_tuple = state.to_tuple()

        # Track expanded node & update depth
        expanded_nodes.append(copy.deepcopy(state.board))
        max_depth = max(max_depth, state.depth)
        frontier_dict.pop(state_tuple, None)
        explored.add(state_tuple)

        if trace:
            true_dist = calculate_true_distance(state,goal_state)
            trace_data.append({
                'step': step,
                'action': 'dequeue',
                'current_state': copy.deepcopy(state.board),
                'g_cost': current_node.g_cost,
                'h_cost': current_node.h_cost,
                'f_cost': current_node.f_cost,
                'true_distance' : true_dist,
                'depth': state.depth,
                'frontier_size': len(frontier),
                'explored_size': len(explored),
                'message': f"Dequeued node with f={current_node.f_cost:.2f}"
            })

        # Goal test
        if state == goal_state:
            solution_path = reconstruct_path(state)
            if trace:
                trace_data.append({
                    'step': step + 1,
                    'action': 'goal_found',
                    'current_state': copy.deepcopy(state.board),
                    'total_cost': current_node.g_cost,
                    'message': 'Goal reached!'
                })
                return solution_path, trace_data, expanded_nodes, max_depth, heuristic_name
            return solution_path

        # Expand neighbors
        neighbors = state.get_neighbors()
        added_count, updated_count = 0, 0
        
        for neighbor in neighbors:
            neighbor_tuple = neighbor.to_tuple()
            if neighbor_tuple in explored:
                continue

            # Calculate costs
            g_cost = current_node.g_cost + 1
            h_cost = heuristic_func(neighbor.board, goal_state.board)
            neighbor_node = AStarNode(neighbor, g_cost, h_cost)

            if neighbor_tuple not in frontier_dict:
                heapq.heappush(frontier, neighbor_node)
                frontier_dict[neighbor_tuple] = neighbor_node
                added_count += 1
            else:
                existing_node = frontier_dict[neighbor_tuple]
                if g_cost < existing_node.g_cost:
                    # Update costs and parent for a better route
                    existing_node.g_cost = g_cost
                    existing_node.h_cost = h_cost
                    existing_node.f_cost = g_cost + h_cost
                    existing_node.state.parent = state
                    existing_node.state.move = neighbor.move
                    existing_node.state.depth = state.depth + 1
                    heapq.heapify(frontier)
                    updated_count += 1

        if trace and (added_count or updated_count):
            trace_data.append({
                'step': step,
                'action': 'expand',
                'added_neighbors': added_count,
                'updated_neighbors': updated_count,
                'frontier_size': len(frontier),
                'explored_size': len(explored),
                'message': f'Expanded {added_count} added, {updated_count} updated nodes'
            })

    if trace:
        trace_data.append({'step': step + 1, 'action': 'failed', 'message': 'No solution exists'})
        return None, trace_data, expanded_nodes, max_depth, heuristic_name
    return None


def print_astar_solution(solution, trace, heuristic_name):
    """Pretty print A* solution with trace information."""
    if not solution:
        print("\nNo solution found!")
        return
    
    print(f"\nUsing {heuristic_name}")
    print(f"States explored: {trace[-2]['explored_size'] if len(trace) > 1 else 0}")
    print(f"\nSolution found with {len(solution) - 1} moves:")
    print("="*50)
    
    for i, step in enumerate(solution):
        if step['move']:
            print(f"\nMove {i}: {step['move']}")
        else:
            print(f"\nStep {i}: Initial State")
        
        board_str = '\n'.join([' '.join(map(str, row)) for row in step['board']])
        print(board_str)
    
    print("\n" + "="*50)
    
    # Print detailed trace information
    print("\nDetailed Trace (Admissibility Check):")
    print("-"*95)
    print(f"{'Step':<6} {'Action':<12} {'g(n)':<6} {'h(n)':<8} {'f(n)':<8} {'True d*':<9} {'Admissible':<12} {'Frontier':<10} {'Explored':<10}")
    print("-"*95)
    
    for entry in trace:
        step = entry.get('step', 0)
        action = entry.get('action', 'N/A')
        g_cost = entry.get('g_cost', 0)
        h_cost = entry.get('h_cost', 0)
        f_cost = entry.get('f_cost', 0)
        true_distance = entry.get('true_distance', None)
        frontier_size = entry.get('frontier_size', 0)
        explored_size = entry.get('explored_size', 0)
        
        if action == 'dequeue' and true_distance is not None:
            admissible = "Yes" if h_cost <= true_distance else "No"
            print(f"{step:<6} {action:<12} {g_cost:<6} {h_cost:<8.2f} {f_cost:<8.2f} {true_distance:<9} {admissible:<12} {frontier_size:<10} {explored_size:<10}")
