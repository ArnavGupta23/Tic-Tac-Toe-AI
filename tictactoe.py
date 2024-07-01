"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Count the number of X's and O's on the board
    counterX = 0
    counterO = 0

    for row in board:
        counterX += row.count(X)
        counterO += row.count(O)

    # If X has more moves, it's O's turn; otherwise, it's X's turn
    if counterX > counterO:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    
    # Iterate over the board and add empty positions to the set of possible actions
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                possible_actions.add((row, col))
    
    return possible_actions
            

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Determine the player making the move
    player_move = player(board)
    newBoard_copy = copy.deepcopy(board)
    row, col = action

    # Raise an exception if the action is invaild
    if action not in actions(board):
        raise Exception("Invalid Action")
    
    # Apply the move to the 
    newBoard_copy[row][col] = player_move
    return newBoard_copy
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for player in (X, O):
        # Check rows for a win
        for row in board:
            if all(cell == player for cell in row):
                return player
        
        # Check columns for a win
        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return player
        
        # Check diagonals for a win
        if all(board[i][i] == player for i in range(3)):
            return player
        if all(board[i][2 - i] == player for i in range(3)):
            return player

    # If no winner, return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Game is won by one of the players
    if winner(board) != None:
        return True
    
    # Game in progress
    for row in board:
        if EMPTY in row:
            return False

    # Game ended
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    win_player = winner(board)

    if win_player == X:
        return 1
    elif win_player == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def max_value(state):
        # Initialize the value to negative infinity
        v = -math.inf
        best_move = None
        
        # If the state is terminal, return its utility
        if terminal(state):
            return utility(state), best_move
        
        # Iterate over all possible actions
        for action in actions(state):
            # Calculate the minimum value for the resulting state
            min_val, _ = min_value(result(state, action))
            
            # Update the value and best move if a higher value is found
            if min_val > v:
                v = min_val
                best_move = action
                
        return v, best_move

    def min_value(state):
        # Initialize the value to positive infinity
        v = math.inf
        best_move = None
        
        # If the state is terminal, return the utility
        if terminal(state):
            return utility(state), best_move
        
        # Iterate over all possible actions
        for action in actions(state):
            # Calculate the maximum value for the resulting state
            max_val, _ = max_value(result(state, action))
            
            # Update the value and best move if a lower value is found
            if max_val < v:
                v = max_val
                best_move = action
                
        return v, best_move

    # Determine the current player
    current_player = player(board)

    # If the game is over, return None
    if terminal(board):
        return None

    # Choose the best move for the current player
    if current_player == X:
        _, move = max_value(board)
    else:
        _, move = min_value(board)
    
    return move