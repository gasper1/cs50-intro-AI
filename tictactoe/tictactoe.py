"""
Tic Tac Toe Player
"""
import copy
import math

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
    how_many_X = sum([int(cell == "X") for row in board for cell in row])
    how_many_O = sum([int(cell == "O") for row in board for cell in row])
    return X if (how_many_X + how_many_O) % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is None:
                possible_moves.add((i, j))
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    if board_copy[action[0]][action[1]] is not None:
        raise ValueError
    if action is not None:
        if max(action) > 2 and min(action) < 0:
            raise ValueError
        board_copy[action[0]][action[1]] = player(board_copy)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check if X won
    match_X = [[int(cell == X) for cell in row] for row in board]
    match_X_T = [[row[i] for row in match_X] for i in
                 range(len(match_X[0]))]  # Transposed match_X - to iterate through columns rather than rows

    # X - ROWS and COLUMNS - Check winning combinations
    row_total_X = [sum(rowX) for rowX in match_X]
    col_total_X = [sum(colX) for colX in match_X_T]
    if max(row_total_X) == 3 or max(col_total_X) == 3:
        return X

    # X - DIAGONAL - Check winning combinations
    sum_diag_1_X = match_X[0][0] + match_X[1][1] + match_X[2][2]
    if sum_diag_1_X == 3:
        return X
    sum_diag_2_X = match_X[0][2] + match_X[1][1] + match_X[2][0]
    if sum_diag_2_X == 3:
        return X

    # Check if O won
    match_O = [[int(cell == O) for cell in row] for row in board]
    match_O_T = [[row[i] for row in match_O] for i in
                 range(len(match_O[0]))]  # Transposed match_O - to iterate through columns rather than rows

    # O - ROWS and COLUMNS - Check winning combinations
    row_total_O = [sum(rowO) for rowO in match_O]
    col_total_O = [sum(colO) for colO in match_O_T]
    if max(row_total_O) == 3 or max(col_total_O) == 3:
        return O

    # O - DIAGONAL - Check winning combinations
    sum_diag_1_O = match_O[0][0] + match_O[1][1] + match_O[2][2]
    if sum_diag_1_O == 3:
        return O
    sum_diag_2_O = match_O[0][2] + match_O[1][1] + match_O[2][0]
    if sum_diag_2_O == 3:
        return O

    # If no one wins
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    how_many_None = sum([int(cell is None) for row in board for cell in row])
    if how_many_None == 0 or winner(board) is not None:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def minimax_old(board):
    """
    Returns the optimal action for the current player on the board.
    """
    optimal_move = None
    # If game finished, no moves available ==> skip all the code below and return None (i.e. optimal_move)
    if not terminal(board):
        # Otherwise evaluate the utility of the available moves and pick the optimal
        # Define evaluation criteria for the current player
        if player(board) == O:
            # O playing --> minimizes utility
            optimal_move_utility = 100
            best_possible_utility = -1
            optimization_func = lambda current_utility, best_utility: current_utility < best_utility
        else:
            # X playing --> maximizes utility
            optimal_move_utility = -100
            best_possible_utility = 1
            optimization_func = lambda current_utility, best_utility: current_utility > best_utility
        # Find optimal move based on current player criteria
        for available_move in actions(board):
            next_board = result(board, available_move)
            move_utility = utility(next_board)
            if not terminal(next_board):
                next_next_board = result(next_board, minimax(next_board))
                move_utility += utility(next_next_board)
                if board == [[None, 'O', None], [None, None, 'X'], ['X', None, None]]:
                    print(player(board) + '- Move: ' + str(available_move) + ' Util: ' + str(move_utility))
            if optimization_func(move_utility, optimal_move_utility):
                optimal_move = available_move
                optimal_move_utility = move_utility
                if optimal_move_utility == best_possible_utility:
                    break
    return optimal_move


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == O:
        optimal_move = min_value(board)[1]
    else:
        optimal_move = max_value(board)[1]
    return optimal_move


def min_value(board):
    move_utility = 100
    move = None
    if terminal(board):
        return utility(board), None
    for available_move in actions(board):
        prev_move_utility = move_utility
        next_board = result(board, available_move)
        move_utility = min(move_utility, max_value(next_board)[0])
        if move_utility != prev_move_utility:
            move = available_move
    return move_utility, move


def max_value(board):
    move_utility = -100
    move = None
    if terminal(board):
        return utility(board), None
    for available_move in actions(board):
        prev_move_utility = move_utility
        next_board = result(board, available_move)
        move_utility = max(move_utility, min_value(next_board)[0])
        if move_utility != prev_move_utility:
            move = available_move
    return move_utility, move
