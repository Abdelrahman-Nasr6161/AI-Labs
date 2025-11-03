from puzzleState import PuzzleState, reconstruct_path
import copy

def IDDFS(initialState, goalState, max_depth_limit=35, trace=False):
    """
    Iterative Deepening DFS for 8-puzzle.
    Args:
        initialState : PuzzleState (initial configuration)
        goalState : PuzzleState (goal configuration)
        max_depth_limit : maximum depth limit for IDDFS
        trace : if True, collects debugging trace data
    Returns:
        (solution_path, trace_data, expanded_nodes, max_depth) if found
        (None, trace_data, expanded_nodes, max_depth) if not found
    """
    expanded_nodes = []
    expanded_set = set()
    trace_data = []
    max_depth_reached = 0
    step = 0
    
    for limit in range(max_depth_limit + 1):
        if trace:
            trace_data.append({
                'step': step,
                'action': 'start_iteration',
                'depth_limit': limit,
                'message': f'Starting DFS with depth limit {limit}'
            })
        
        solution, found, depth_reached = depth_limited_DFS(
            initialState, goalState, limit,
            expanded_nodes, expanded_set, trace_data, trace
        )
        
        max_depth_reached = max(max_depth_reached, depth_reached)
        
        if found:
            if trace:
                trace_data.append({
                    'step': step + 1,
                    'action': 'goal_found',
                    'message': f'Goal found at depth {limit}'
                })
            return solution, trace_data, expanded_nodes, max_depth_reached
        
        step += 1
    
    if trace:
        trace_data.append({
            'step': step,
            'action': 'no_solution',
            'message': f'No solution found up to depth {max_depth_limit}'
        })
    
    return None, trace_data, expanded_nodes, max_depth_reached


def depth_limited_DFS(state, goalState, limit,
                      expanded_nodes, expanded_set,
                      trace_data, trace=False):
    """
    Performs depth-limited DFS with depth-aware exploration.
    Key modification: Track explored states WITH their depths to allow
    revisiting at different depths for optimality.
    """
    frontier = [state]
    frontier_set = {state.to_tuple()}
    explored = {}  # Changed: now maps state_tuple -> depth at which it was explored
    max_depth = 0
    step = 0
    
    while frontier:
        current_state = frontier.pop()
        current_tuple = current_state.to_tuple()
        frontier_set.discard(current_tuple)
        
        # Skip if already explored at THIS depth or shallower
        if current_tuple in explored and explored[current_tuple] <= current_state.depth:
            continue
        
        # Mark as explored at this depth
        explored[current_tuple] = current_state.depth
        
        # Track for global expanded nodes
        if current_tuple not in expanded_set:
            expanded_nodes.append(current_state.board.copy())
            expanded_set.add(current_tuple)
        
        max_depth = max(max_depth, current_state.depth)
        
        if trace:
            trace_data.append({
                'step': step,
                'action': 'pop',
                'current_state': current_state.board.copy(),
                'depth': current_state.depth,
                'frontier_size': len(frontier),
                'explored_size': len(explored),
                'message': f"Popped node at depth {current_state.depth} (limit {limit})"
            })
        
        # Goal test
        if current_state == goalState:
            return reconstruct_path(current_state), True, max_depth
        
        # Expand if under depth limit
        if current_state.depth < limit:
            for neighbor in reversed(current_state.get_neighbors()):
                neighbor_tuple = neighbor.to_tuple()
                neighbor_depth = current_state.depth + 1
                
                # Allow adding if:
                # 1. Never explored before, OR
                # 2. Previously explored but at a GREATER depth (found a shorter path)
                if (neighbor_tuple not in explored or 
                    explored[neighbor_tuple] > neighbor_depth) and \
                   neighbor_tuple not in frontier_set:
                    frontier.append(neighbor)
                    frontier_set.add(neighbor_tuple)
        
        step += 1
    
    return None, False, max_depth