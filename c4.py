#import libraries
from os import system, name
import sys
from math import floor
from time import sleep

#text color/style
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
#how many in a row to win
how_many_to_connect = 4


#coninuesly ask for input until something valid is input
def ask_for_input(input_text, conv):
    while True:
        try:
            a = input(input_text)
            if not a:
                continue
            else:
                ans = conv.replace('THE_INPUT', a)
                ans = eval(str(ans))
                return ans
        except (NameError, ValueError, KeyError, TypeError) as e:
            continue

#set the colors/styles/column count/row count from input
background_color = (text_color['black'] + 10)
ROW_COUNT = 1 + ask_for_input(input_text='How many rows should there be?\n', conv='int(str(THE_INPUT))')
COLUMN_COUNT = ask_for_input(input_text='How many columns should there be?\n', conv='int(str(THE_INPUT))')
player_1_color = ask_for_input(input_text="What should be the color for player 1?\n(R)ed, (G)reen, (Y)ellow, (B)lue, (P)urple, (C)yan, (W)hite\n", conv="text_color[str.lower(str('THE_INPUT'))]")
player_2_color = ask_for_input(input_text="What should be the color for player 2?\n(R)ed, (G)reen, (Y)ellow, (B)lue, (P)urple, (C)yan, (W)hite\n", conv="text_color[str.lower(str('THE_INPUT'))]")
player_1_style = ask_for_input(input_text="What should be the style for player 1?\n(N)one, (B)old, (I)talic, (U)nderline\n", conv="text_style[str.lower(str('THE_INPUT'))]")
player_2_style = ask_for_input(input_text="What should be the style for player 2?\n(N)one, (B)old, (I)talic, (U)nderline\n", conv="text_style[str.lower(str('THE_INPUT'))]")
#player_to_help = ask_for_input(input_text='', conv='int(THE_INPUT)')


#class for the board obj
class Board:
    def __init__(self, x, y, state, winner):
        self.winner = winner
        self.x, self.y = x, y
        self.state = state


#function to create a board
def create_board():
    #create 2 dimensional array
    state = [0] * ROW_COUNT
    for i in range(ROW_COUNT):
        state[i] = [0] * COLUMN_COUNT

    #return the array
    board = Board(x=0, y=0, state=state, winner=0)
    return board


#function to put a piece on the board
def drop_piece(board, row, col, piece):
    board.state[row][col] = piece


#validate the location to drop a piece
def is_valid_location(board, col):
    return board.state[ROW_COUNT - 1][col] == 0


#find the lowest open row on a given column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board.state[r][col] == 0:
            return r


#print the board to the terminal
def print_board(board):
    #print column numbers
    for i in range(1, COLUMN_COUNT + 1):
        print(str(i), end=' ' * (5 + 1 - len(str(i))))
    #print a new line
    print('')
    #loop through all coolumns on the board
    for y in reversed(range(COLUMN_COUNT - 1)):
        #if scale > 1 then we wil print multiple rows
        for i in range(0, 3):
            #loop through all rows on the board
            for x in range(ROW_COUNT):
                #check if the current field s filled by player 1
                if str(int(board.state[y][x])) == '1':
                    #set the printing color and style to the one of player 1
                    print(str("\033[" + str(player_1_style) + ";" + str(player_1_color) + ";" + str(background_color) + "m"), end='')
                #check if the current field s filled by player 2
                elif str(int(board.state[y][x])) == '2':
                    #set the printing color and style to the one of player 2
                    print(str("\033[" + str(player_2_style) + ";" + str(player_2_color) + ";" + str(background_color) + "m"), end='')
                #this means the field is empty
                else:
                    #print in blue
                    print("\033[1;34;40m", end='')
                #print the players number or a 0 for an empty field
                print(str(int(board.state[y][x])) * 5, end='')
                #switch the printing color to white again
                print("\033[1;37;40m", end='')
                print(' ', end='')
            print('')
        print('')
    #print column numbers at the bottom
    for i in range(1, COLUMN_COUNT + 1):
        print(str(i), end=' ' * (5 + 1 - len(str(i))))
    print('')


def is_there_a_winning_move(board, piece):
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, piece)
            if winning_move(board, piece):
                print('Player {0} can win in one move by placing a piece in column {1}'.format(piece, col + 1))
                sleep(5)
            board.state[row][col] = 0

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - (how_many_to_connect - 1)):
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
        for r in range(ROW_COUNT - (how_many_to_connect - 1)):
            win = True
            for i in range(how_many_to_connect):
                if board.state[r + i][c] != piece:
                    win = False
                    break
            if win:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - (how_many_to_connect - 1)):
        for r in range(ROW_COUNT - (how_many_to_connect - 1)):
            win = True
            for i in range(how_many_to_connect):
                if board.state[r + i][c + i] != piece:
                    win = False
                    break
            if win:
                return True

    for c in range(COLUMN_COUNT - (how_many_to_connect - 1)):
        for r in range((how_many_to_connect - 1), ROW_COUNT):
            win = True
            for i in range(how_many_to_connect):
                if board.state[r - i][c + i] != piece:
                    win = False
                    break
            if win:
                return True


#clear the screen
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
# for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


#this is the loop that keeps the game running
def game_loop(board, big_board):
    turn = 0
    game_over = False
    while not game_over:
        clear()
        print_board(board)
        #print who's turn it is
        print("\nPlayer {}'s turn: ".format(turn + 1), end='')
        col = (ask_for_input(input_text='', conv='int(THE_INPUT)') - 1) % COLUMN_COUNT
        if is_valid_location(board, col):
            #if the column is valid then we find the lowest available row
            row = get_next_open_row(board, col)
            if big_board == True:
                #if this is the big gameboard then we play a game at the givin column at the lowest row
                game_loop(boards[row][col], False)
            else:
                #if this is a small gameboard then we drop a piece on the board
                drop_piece(board, row, col, turn + 1)
                clear() 
                print_board(board)

                #if the player who just dropped a piece made a winning move then we end the game and display the winner
                if winning_move(board, turn + 1):
                    game_over = True
                    print("Player {} has won".format(turn + 1))
                #else:
                    #is_there_a_winning_move(board, 2 - turn)

        #change turns
        turn = 1 - turn

#make an array of boards(big game_board)
n = ROW_COUNT + 1
m = COLUMN_COUNT + 1
boards = [0] * n
for i in range(n):
    boards[i] = [0] * m

for i in range(ROW_COUNT):
    for j in range(COLUMN_COUNT):
        boards[i][j] = create_board()

#start the game loop
game_loop(board=boards[0][0], big_board=False)
