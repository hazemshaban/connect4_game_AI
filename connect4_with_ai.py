import numpy as np
import random
import pygame
import sys
import math
from future.moves import tkinter
from tkinter import *

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

algo_type=0
PLAYER = 0
AI = 1

AI_COUNT=0
PLAYER_COUNT=0
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

#create board using numy arrays and filling it all with zero values
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

#effect of dropping a piece on the array
def drop_piece(board, row, col, piece):
    board[row][col] = piece

#checking valid locations and returning it
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(str(np.flip(board, 0))+"\n")

#checking for all possible winning moves
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True

#evaluation for the AI on the whole board (heuristic)
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2


    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 5
    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
        score -= 2
    elif window.count(opp_piece) == 4 and window.count(EMPTY) == 0:
        score -= 100

    return score

#updating the score after palying any move for the AI to check for the best move
def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

#checking space on board
def is_terminal_node(board):
    return  len(get_valid_locations(board)) == 0

#applying minimax algorithm
def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            print(str(np.flip(b_copy, 0)) + "\n"+str(col))
            new_score = minimax(b_copy,depth-1,False)[1]
            if new_score > value:
                value=new_score
                column=col
        return column,value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            print(str(np.flip(b_copy, 0)) + "\n" + str(col))
            new_score = minimax(b_copy, depth - 1, False)[1]
            if new_score < value:
                value = new_score
                column = col

        return column,value

#minimax with alpha beta pruning
def minimax_Alph_peta(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            print(str(np.flip(b_copy, 0)) + "\n" + str(col))
            new_score = minimax_Alph_peta(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            print(str(np.flip(b_copy, 0)) + "\n" + str(col))
            new_score = minimax_Alph_peta(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value



#return locations that are empty
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

#determining the best ove for th eAI by checking the score after theoritaclly playing it
def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col



def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

#setting the environment for program excution
board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 50)

turn = random.randint(PLAYER, AI)

root = tkinter.Tk()

root.title('algo')

root.geometry('200x100')

alpha_prun = tkinter.IntVar()

def end(root, var):
    print(var.get())
    root.destroy()

radioButton1 = Radiobutton(root, text='with pruning',variable = alpha_prun,value = 0, command = lambda: end(root,alpha_prun))
radioButton2 = Radiobutton(root, text='without pruning',variable = alpha_prun,value = 1, command = lambda: end(root, alpha_prun))

radioButton1.pack()
radioButton2.pack()

root.mainloop()

#function for counting all the winning moves for each player
def connections_count(board, attribute):
    count = 0
    # Check horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == attribute \
                    and board[r][c + 1] == attribute \
                    and board[r][c + 2] == attribute \
                    and board[r][c + 3] == attribute:
                count += 1

    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == attribute \
                    and board[r + 1][c] == attribute \
                    and board[r + 2][c] == attribute \
                    and board[r + 3][c] == attribute:
                count += 1

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == attribute \
                    and board[r + 1][c + 1] == attribute \
                    and board[r + 2][c + 2] == attribute \
                    and board[r + 3][c + 3] == attribute:
                count += 1

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == attribute \
                    and board[r - 1][c + 1] == attribute \
                    and board[r - 2][c + 2] == attribute \
                    and board[r - 3][c + 3] == attribute:
                count += 1
    return count

#main loop where the player and AI engage in the game
while not is_terminal_node(board):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # Ask for Player 1 Input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):

                        if is_terminal_node(board):
                            PLAYER_COUNT=connections_count(board,PLAYER_PIECE)
                            AI_COUNT = connections_count(board, AI_PIECE)

                            if AI_COUNT < PLAYER_COUNT:
                                label = myfont.render("HUMAN:"+str(PLAYER_COUNT)+" AI:" + str(AI_COUNT), 1, RED)
                            elif AI_COUNT > PLAYER_COUNT:
                                label = myfont.render("AI:" + str(AI_COUNT)+" HUMAN:"+str(PLAYER_COUNT), 1, RED)
                            screen.blit(label, (5, 10))
                            game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)

    # # Ask for Player 2 Input
    if turn == AI and not game_over:

        # col = random.randint(0, COLUMN_COUNT-1)
        # col = pick_best_move(board, AI_PIECE)
        if alpha_prun.get()==0:
            col, minimax_score = minimax_Alph_peta(board, 5, -math.inf, math.inf, True)
        else:
            col, minimax_score = minimax(board, 5, True)
        if is_valid_location(board, col):
            # pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):

                if is_terminal_node(board):
                    PLAYER_COUNT = connections_count(board, PLAYER_PIECE)
                    AI_COUNT = connections_count(board, AI_PIECE)
                    if AI_COUNT<PLAYER_COUNT:
                        label = myfont.render("HUMAN:"+str(PLAYER_COUNT)+" AI:" + str(AI_COUNT), 1, RED)
                    elif AI_COUNT >PLAYER_COUNT:
                        label = myfont.render("AI:" + str(AI_COUNT)+" HUMAN:"+str(PLAYER_COUNT), 1, RED)

                    screen.blit(label, (5, 10))
                    game_over = True

            print_board(board)
            draw_board(board)
            #print(AI_COUNT)
            #print(PLAYER_COUNT)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(7000)