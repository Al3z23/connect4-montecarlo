import numpy as np
import math

ROWS, COLS = 6, 7
PLAYER, CPU = 1, 2
WINNING_LENGTH = 4

def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROWS - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Check horizontal
    for c in range(COLS - 3):
        for r in range(ROWS):
            if all(board[r][c+i] == piece for i in range(WINNING_LENGTH)):
                return True
    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(WINNING_LENGTH)):
                return True
    # Check positive diagonal
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if all(board[r+i][c+i] == piece for i in range(WINNING_LENGTH)):
                return True
    # Check negative diagonal
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == piece for i in range(WINNING_LENGTH)):
                return True
    return False

def evaluate_window(window, piece):
    opp_piece = PLAYER if piece == CPU else CPU
    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 5
    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 80
    return score

def score_position(board, piece):
    score = 0
    # Prefer center column
    center_array = [int(i) for i in list(board[:, COLS//2])]
    score += center_array.count(piece) * 6
    # Score horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLS - 3):
            window = row_array[c:c+WINNING_LENGTH]
            score += evaluate_window(window, piece)
    # Score vertical
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r+WINNING_LENGTH]
            score += evaluate_window(window, piece)
    # Score diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(WINNING_LENGTH)]
            score += evaluate_window(window, piece)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(WINNING_LENGTH)]
            score += evaluate_window(window, piece)
    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER) or winning_move(board, CPU) or len(get_valid_locations(board)) == 0

def get_valid_locations(board):
    return [c for c in range(COLS) if is_valid_location(board, c)]

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)
    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, CPU):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER):
                return (None, -10000000000000)
            else: # Empate
                return (None, 0)
        else:
            return (None, score_position(board, CPU))
    if maximizingPlayer:
        value = -math.inf
        best_col = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, CPU)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        best_col = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value


# Ejemplo de uso
board = create_board()
game_over = False

while not game_over:
    # Turno jugador
    col = int(input("Elige columna (0-6): "))
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, PLAYER)

    if winning_move(board, PLAYER):
        print("Ganaste!")
        game_over = True
        break

    # Turno CPU (minimax)
    col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, CPU)

    print(board)

    if winning_move(board, CPU):
        print("CPU gana!")
        game_over = True
        break
