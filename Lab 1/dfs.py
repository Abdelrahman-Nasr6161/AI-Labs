from puzzleState import PuzzleState, reconstruct_path
import copy

def DFS(initialState, goalState):
    """    
    Args:
        initialState: PuzzleState object representing the start
        goalState: PuzzleState object representing the goal
    
    Returns:
        (solution_path, trace_data, expanded_nodes, max_depth)
    """
    frontier = [initialState]           # Stack for DFS
    frontier_set = {initialState.to_tuple()}  # Set for O(1) frontier membership check
    explored = set()
    expanded_nodes = []
    trace_data = []
    max_depth = 0

    trace_data.append({
        'step': 0,
        'action': 'initialize',
        'current_state': copy.deepcopy(initialState.board),
        'frontier_size': 1,
        'explored_size': 0,
        'message': 'Starting DFS with initial state'
    })
    
    step = 0
    
    while frontier:
        step += 1
        state = frontier.pop()  # LIFO for DFS
        state_tuple = state.to_tuple()
        
        # Defensive removal from frontier_set
        if state_tuple in frontier_set:
            frontier_set.remove(state_tuple)

        expanded_nodes.append(copy.deepcopy(state.board))
        max_depth = max(max_depth, state.depth)

        trace_data.append({
            'step': step,
            'action': 'pop',
            'current_state': copy.deepcopy(state.board),
            'depth': state.depth,
            'move': state.move,
            'frontier_size': len(frontier),
            'explored_size': len(explored),
            'message': f'Popped state (depth {state.depth})'
        })

        if state == goalState:
            solution_path = reconstruct_path(state)
            trace_data.append({
                'step': step + 1,
                'action': 'goal_found',
                'current_state': copy.deepcopy(state.board),
                'solution_length': len(solution_path),
                'message': f'Goal found! Solution has {len(solution_path)} moves'
            })
            return solution_path, trace_data, expanded_nodes, max_depth
        
        explored.add(state_tuple)

        neighbors = state.get_neighbors()
        added_count = 0

        for neighbor in neighbors:
            neighbor_tuple = neighbor.to_tuple()
            
            # Use hashed checks for both frontier and explored
            if neighbor_tuple not in explored and neighbor_tuple not in frontier_set:
                frontier.append(neighbor)
                frontier_set.add(neighbor_tuple)
                added_count += 1

        if added_count > 0:
            trace_data.append({
                'step': step,
                'action': 'expand',
                'added_neighbors': added_count,
                'frontier_size': len(frontier),
                'explored_size': len(explored),
                'message': f'Added {added_count} new neighbors to frontier'
            })

    trace_data.append({
        'step': step + 1,
        'action': 'failed',
        'message': 'Goal not found - no solution exists'
    })
    return None, trace_data, expanded_nodes, max_depth
