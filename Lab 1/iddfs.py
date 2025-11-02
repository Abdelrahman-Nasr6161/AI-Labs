from collections import deque
from puzzleState import PuzzleState, reconstruct_path
import copy

def IDDFS(initialState, goalState):
    """    
    Args:
        initialState: PuzzleState object representing the start
        goalState: PuzzleState object representing the goal
    
    Returns:
        (solution_path, trace_data, expanded_nodes, max_depth)
    """
    max_depth = 0
    expanded_nodes = []  # All unique expanded nodes across all depths
    trace_data = []      # Step-by-step trace
    depth_limit = 0      # Start depth limit
    
    step = 0
    
    while True:
        # Add iteration start to trace
        trace_data.append({
            'step': step,
            'action': 'start_iteration',
            'depth_limit': depth_limit,
            'message': f'Starting DFS with depth limit {depth_limit}'
        })
        
        # Perform depth-limited DFS
        result = depth_limited_DFS(initialState, goalState, depth_limit, expanded_nodes, trace_data, step)
        solution_path, found, max_depth_reached = result
        
        max_depth = max(max_depth, max_depth_reached)
        
        if found:  # Goal achieved
            trace_data.append({
                'step': step + 1,
                'action': 'goal_found',
                'message': f'Goal found at depth {depth_limit}'
            })
            return solution_path, trace_data, expanded_nodes, max_depth
        
        # If no solution found at this depth, increment depth
        depth_limit += 1
        step += 1

def depth_limited_DFS(state, goalState, limit, expanded_nodes, trace_data, step):
    """DFS within a limited depth"""
    frontier = [state]
    explored = set()
    max_depth = 0
    
    while frontier:
        current_state = frontier.pop()
        
        # Track expanded node only if not already counted
        if current_state.board not in expanded_nodes:
            expanded_nodes.append(copy.deepcopy(current_state.board))
        
        max_depth = max(max_depth, current_state.depth)
        
        # Skip if beyond the limit
        if current_state.depth > limit:
            continue
        
        # Trace data
        trace_data.append({
            'step': step,
            'action': 'pop',
            'current_state': copy.deepcopy(current_state.board),
            'depth': current_state.depth,
            'move': current_state.move,
            'frontier_size': len(frontier),
            'explored_size': len(explored),
            'message': f'Popped state at depth {current_state.depth}, within limit {limit}'
        })
        
        # Check if goal reached
        if current_state == goalState:
            solution_path = reconstruct_path(current_state)
            return solution_path, True, max_depth
        
        explored.add(current_state.to_tuple())
        
        # Get neighbors (DFS order: deepest neighbors first)
        neighbors = current_state.get_neighbors()
        for neighbor in reversed(neighbors):  # Reverse for correct DFS order
            neighbor_tuple = neighbor.to_tuple()
            if neighbor_tuple not in explored:
                frontier.append(neighbor)
        
        step += 1
    
    return None, False, max_depth  # Not found at this depth
