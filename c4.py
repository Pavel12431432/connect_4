from os import system, name
import sys
from math import floor
from time import sleep

scale = 5
text_color = {
    'black': 30,
    'r': 31,
    'g': 32,
    'y': 33,
    'b': 34,
    'p': 35,
    'c': 36,
    'w': 37,
}
text_style = {
    'n': 0,
    'b': 1,
    'i': 3,
    'u': 4,
}
background_color = (text_color['black'] + 10)
how_many_to_connect = 4
ROW_COUNT = 1 + 6  #int(input("How many rows should there be?\n"))
COLUMN_COUNT = 7  #int(input("How many columns should there be?\n"))
player_1_color = text_color['r']  #text_color[str.lower(input("What should be the color for player 1?\n(R)ed, (G)reen, (Y)ellow, (B)lue, (P)urple, (C)yan, (W)hite\n"))]
player_2_color = text_color['y']  #text_color[str.lower(input("What should be the color for player 2?\n(R)ed, (G)reen, (Y)ellow, (B)lue, (P)urple, (C)yan, (W)hite\n"))]
player_1_style = text_color['b']  #text_color[str.lower(input("What should be the style for player 1?\n(N)one, (B)old, (I)talic, (U)nderline\n"))]
player_2_style = text_color['b']  #text_color[str.lower(input("What should be the style for player 2?\n(N)one, (B)old, (I)talic, (U)nderline\n"))]


class Board:
    def __init__(self, x, y, state, winner):
        self.winner = winner
        self.x, self.y = x, y
        self.state = state


def create_board():
    state = [0] * ROW_COUNT
    for i in range(ROW_COUNT):
        state[i] = [0] * COLUMN_COUNT

    board = Board(x=0, y=0, state=state, winner=0)
    return board


def drop_piece(board, row, col, piece):
    board.state[row][col] = piece


def is_valid_location(board, col):
    return board.state[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board.state[r][col] == 0:
            return r


def print_board(board):
    for i in range(1, COLUMN_COUNT + 1):
        print(str(i), end=' ' * (scale + 1 - len(str(i))))
    print('')
    for y in reversed(range(COLUMN_COUNT - 1)):
        for i in range(0, scale):
            #for i in range(0, 1):
            for x in range(ROW_COUNT):
                if str(int(board.state[y][x])) == '1':
                    print(str("\033[" + str(player_1_style) + ";" + str(player_1_color) + ";" + str(background_color) + "m"), end='')
                elif str(int(board.state[y][x])) == '2':
                    print(str("\033[" + str(player_2_style) + ";" + str(player_2_color) + ";" + str(background_color) + "m"), end='')
                else:
                    print("\033[1;34;40m", end='')
                print(str(int(board.state[y][x])) * scale, end='')
                print("\033[1;37;40m", end='')
                print(' ', end='')
            print('')
        print('')
    for i in range(1, COLUMN_COUNT + 1):
        print(str(i), end=' ' * (scale + 1 - len(str(i))))
    print('')


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - how_many_to_connect):
        for r in range(ROW_COUNT):
            win = True
            for i in range(how_many_to_connect):
                if board.state[r][c + i] != piece:
                    win = False
                    break
            if win:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - how_many_to_connect):
            win = True
            for i in range(how_many_to_connect):
                if board.state[r + i][c] != piece:
                    win = False
                    break
            if win:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - how_many_to_connect):
        for r in range(ROW_COUNT - how_many_to_connect):
            win = True
            for i in range(how_many_to_connect):
                if board.state[r + i][c + i] != piece:
                    win = False
                    break
            if win:
                return True

    for c in range(COLUMN_COUNT - how_many_to_connect):
        for r in range(how_many_to_connect, ROW_COUNT):
            win = True
            for i in range(how_many_to_connect):
                if board.state[r - i][c + i] != piece:
                    win = False
                    break
            if win:
                return True


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')


# for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def game_loop(board, big_board):
    turn = 0
    game_over = False
    while not game_over:
        clear()
        print_board(board)
        print("\nPlayer {}'s turn: ".format(turn + 1), end='')
        try:
            col = (int(input()) - 1) % COLUMN_COUNT
        except ValueError:
            print("Unknown character")
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            if big_board == True:
                game_loop(boards[row][col], False)
            else:
                drop_piece(board, row, col, turn + 1)
                clear()
                print_board(board)

        if winning_move(board, turn + 1):
            clear()
            print_board(board)
            game_over = True
            print("Player {} has won".format(turn + 1))

        turn = 1 - turn


n = ROW_COUNT + 1
m = COLUMN_COUNT + 1
boards = [0] * n
for i in range(n):
    boards[i] = [0] * m

for i in range(ROW_COUNT):
    for j in range(COLUMN_COUNT):
        boards[i][j] = create_board()

game_loop(board=boards[0][0], big_board=False)
