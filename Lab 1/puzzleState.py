import copy

class PuzzleState:
    def __init__(self, board, parent=None, move=None, depth=0, cost=0):
        self.board = board  # 2D list representing the puzzle
        self.parent = parent
        self.move = move  # Move that led to this state
        self.depth = depth
        self.cost = cost  # For UCS, A*
        self.blank_pos = self.find_blank()
    
    def find_blank(self):
        """Find the position of the blank (0) tile."""
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def get_neighbors(self):
        """Generate all valid neighbor states."""
        neighbors = []
        row, col = self.blank_pos
        moves = [
            ('Up', -1, 0),
            ('Down', 1, 0),
            ('Left', 0, -1),
            ('Right', 0, 1)
        ]
        
        for move_name, dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0]):
                # Create new board by swapping blank with adjacent tile
                new_board = [row.copy() for row in self.board]
                new_board[row][col], new_board[new_row][new_col] = \
                    new_board[new_row][new_col], new_board[row][col]
                
                neighbor = PuzzleState(
                    new_board, 
                    self, 
                    move_name, 
                    self.depth + 1,
                    self.cost + 1  # Each move costs 1
                )
                neighbors.append(neighbor)
        
        return neighbors
    
    def to_tuple(self):
        """Convert board to tuple for hashing."""
        return tuple(tuple(row) for row in self.board)
    
    def __eq__(self, other):
        return self.board == other.board
    
    def __hash__(self):
        return hash(self.to_tuple())
    
    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.board])


def reconstruct_path(state):
    """Reconstruct the solution path from goal to initial state."""
    path = []
    current = state
    
    while current.parent is not None:
        path.append({
            'move': current.move,
            'board': copy.deepcopy(current.board),
            'depth': current.depth
        })
        current = current.parent
    
    # Add initial state
    path.append({
        'move': None,
        'board': copy.deepcopy(current.board),
        'depth': 0
    })
    
    path.reverse()
    return path