import numpy as np
import time
import random
def swap(matrix, i1, j1, i2, j2):
    """Helper function to swap two elements in the matrix."""
    temp = matrix[i1, j1]
    matrix[i1, j1] = matrix[i2, j2]
    matrix[i2, j2] = temp

def solve_dfs_iterative(start_matrix, goal_tuple):
    
    directions = [[-1,0],[0,-1],[1,0],[0,1]] 
    
    stack = []
    stack.append(start_matrix)
    
    explored = set()
    start = time.time()

    while stack:
        current_matrix = stack.pop()
        
        current_tuple = tuple(current_matrix.flatten())

        if current_tuple == goal_tuple:
            print(f"DFS (Iterative) found a solution!")
            print(f"Explored {len(explored)} states.")
            end = time.time()
            return current_matrix , end-start

        if current_tuple in explored:
            continue
            
        explored.add(current_tuple)
        
        i, j = np.where(current_matrix == 0)
        i, j = int(i[0]), int(j[0])


        for move in directions: 
            newI, newJ = i + move[0], j + move[1]

            if 0 <= newI < current_matrix.shape[0] and 0 <= newJ < current_matrix.shape[1]:
                
                matrixPrime = current_matrix.copy()
                swap(matrixPrime, i, j, newI, newJ)
                
                new_tuple = tuple(matrixPrime.flatten())
                
                if new_tuple not in explored:
                    stack.append(matrixPrime)
    end = time.time()
    print(f"DFS (Iterative) could not find a solution after exploring {len(explored)} states.")
    return None , end


if __name__ == "__main__":
    start_state = np.array([1, 2, 5, 3, 4, 0, 6, 7, 8])
    start_state.resize((3, 3))
    
    goal_state_tuple = tuple(np.sort(start_state.flatten()))

    print(f"Starting puzzle:\n{start_state}")
    print(f"Goal state: {goal_state_tuple}\n")

    result , timeE = solve_dfs_iterative(start_state, goal_state_tuple)
    
    if result is not None:
        print("\nSolution Matrix:")
        print(result)
        print(f"\n time taken : {timeE}")