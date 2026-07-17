import math
import random

# -------------------------
# Check Winner
# -------------------------

def check_winner(board):

    wins = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
    ]

    for win in wins:
        a, b, c = win

        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]

    if "" not in board:
        return "Draw"

    return None


# -------------------------
# Minimax Algorithm
# -------------------------

def minimax(board, depth, is_maximizing):

    result = check_winner(board)

    if result == "O":
        return 10 - depth

    elif result == "X":
        return depth - 10

    elif result == "Draw":
        return 0


    if is_maximizing:

        best_score = -math.inf

        for i in range(9):

            if board[i] == "":

                board[i] = "O"

                score = minimax(board, depth + 1, False)

                board[i] = ""

                best_score = max(score, best_score)

        return best_score

    else:

        best_score = math.inf

        for i in range(9):

            if board[i] == "":

                board[i] = "X"

                score = minimax(board, depth + 1, True)

                board[i] = ""

                best_score = min(score, best_score)

        return best_score


# -------------------------
# AI Best Move (50% random, 50% perfect minimax)
# -------------------------

def get_best_move(board):

    empty_cells = [i for i in range(9) if board[i] == ""]

    if not empty_cells:
        return -1

    if random.random() < 0.5:
        return random.choice(empty_cells)

    best_score = -math.inf
    move = -1

    for i in empty_cells:

        board[i] = "O"

        score = minimax(board, 0, False)

        board[i] = ""

        if score > best_score:

            best_score = score
            move = i

    return move
