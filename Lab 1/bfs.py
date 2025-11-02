from collections import deque
from puzzleState import PuzzleState, reconstruct_path
import copy

def BFS(initialState, goalState):
    """    
    Args:
        initialState: PuzzleState object representing the start
        goalState: PuzzleState object representing the goal
    
    Returns:
        (solution_path, trace_data, expanded_nodes, max_depth)
    """
    frontier = deque([initialState])
    explored = set()
    expanded_nodes = []  # Store all expanded states
    trace_data = []      # Store step-by-step information
    max_depth = 0        # Track the deepest node explored

    # Add initial state to trace
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
        state = frontier.popleft()
        
        # Track expanded node
        expanded_nodes.append(copy.deepcopy(state.board))
        max_depth = max(max_depth, state.depth)
        
        # Add to trace
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
        
        # Check if goal
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
        
        explored.add(state.to_tuple())
        
        # Generate neighbors
        neighbors = state.get_neighbors()
        added_count = 0
        
        for neighbor in neighbors:
            neighbor_tuple = neighbor.to_tuple()
            
            # Check if already explored or in frontier
            if neighbor_tuple not in explored:
                # Check if already in frontier
                in_frontier = any(n.to_tuple() == neighbor_tuple for n in frontier)
                
                if not in_frontier:
                    frontier.append(neighbor)
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
    
    # Goal not found
    trace_data.append({
        'step': step + 1,
        'action': 'failed',
        'message': 'Goal not found - no solution exists'
    })
    return None, trace_data, expanded_nodes, max_depth
