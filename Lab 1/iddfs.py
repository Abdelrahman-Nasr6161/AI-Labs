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
    expanded_set = set()  # To track unique boards for expanded_nodes
    trace_data = []
    depth_limit = 0
    step = 0

    while True:
        trace_data.append({
            'step': step,
            'action': 'start_iteration',
            'depth_limit': depth_limit,
            'message': f'Starting DFS with depth limit {depth_limit}'
        })

        result = depth_limited_DFS(
            initialState, goalState, depth_limit,
            expanded_nodes, expanded_set, trace_data, step
        )

        solution_path, found, max_depth_reached = result
        max_depth = max(max_depth, max_depth_reached)

        if found:
            trace_data.append({
                'step': step + 1,
                'action': 'goal_found',
                'message': f'Goal found at depth {depth_limit}'
            })
            return solution_path, trace_data, expanded_nodes, max_depth

        depth_limit += 1
        step += 1


def depth_limited_DFS(state, goalState, limit,
                      expanded_nodes, expanded_set,
                      trace_data, step):
    """Perform DFS up to a specified depth limit."""
    frontier = [state]
    frontier_set = {state.to_tuple()}
    # explored = set()  <--- THIS IS THE BUG. REMOVE IT.
    max_depth = 0

    while frontier:
        current_state = frontier.pop()
        current_tuple = current_state.to_tuple()

        frontier_set.discard(current_tuple)

        if current_tuple not in expanded_set:
            expanded_nodes.append(copy.deepcopy(current_state.board))
            expanded_set.add(current_tuple)

        max_depth = max(max_depth, current_state.depth)

        # Add trace step (do this before any 'continue' or 'return')
        trace_data.append({
            'step': step,
            'action': 'pop',
            'current_state': copy.deepcopy(current_state.board),
            'depth': current_state.depth,
            'move': current_state.move,
            'frontier_size': len(frontier),
            'explored_size': len(expanded_set), # Changed to global expanded_set
            'message': (
                f'Popped state at depth {current_state.depth}, limit {limit}'
            )
        })

        # --- MODIFIED LOGIC ---
        
        # 1. Goal test
        if current_state == goalState:
            solution_path = reconstruct_path(current_state)
            return solution_path, True, max_depth

        # 2. Depth limit check (only expand if *under* the limit)
        if current_state.depth < limit:
            # explored.add(current_tuple) <--- REMOVED
            
            for neighbor in reversed(current_state.get_neighbors()):
                neighbor_tuple = neighbor.to_tuple()
                
                # The only check needed is for the frontier (cycle detection)
                if neighbor_tuple not in frontier_set:
                    frontier.append(neighbor)
                    frontier_set.add(neighbor_tuple)
        
        # If current_state.depth == limit, we did the goal check,
        # but we don't expand its neighbors. We just loop.

        step += 1

    return None, False, max_depth
