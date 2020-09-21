from os import system

how_many_to_connect = 4
background_color = 40
ROW_COUNT = 1 + 6
COL_COUNT = 7
player_1_color = 31
player_2_color = 32
size = (3, 5)

board = [[0] * COL_COUNT for i in range(ROW_COUNT)]


def printBoard():
	system('cls')
	for i in range(1, COL_COUNT + 1):
		print(i, end=' ' * (5 + 1 - len(str(i))))
	print('')
	for y in range(ROW_COUNT):
		for r in range(size[0]):
			for x in range(COL_COUNT):
				if board[y][x] == 1:
					print("\033[1;" + str(player_1_color) + ";" + str(background_color) + "m", end='')
				elif board[y][x] == 2:
					print("\033[1;" + str(player_2_color) + ";" + str(background_color) + "m", end='')
				else:
					print("\033[1;34;40m", end='')
				print('▓' * size[1], end='\033[1;37;40m ')
			print()
		print()


def winning_move(piece):
	for c in range(COL_COUNT - (how_many_to_connect - 1)):
		for r in range(ROW_COUNT):
			win = True
			for i in range(how_many_to_connect):
				if board[r][c + i] != piece:
					win = False
					break
			if win:
				return True

	for c in range(COL_COUNT):
		for r in range(ROW_COUNT - (how_many_to_connect - 1)):
			win = True
			for i in range(how_many_to_connect):
				if board[r + i][c] != piece:
					win = False
					break
			if win:
				return True

	for c in range(COL_COUNT - (how_many_to_connect - 1)):
		for r in range(ROW_COUNT - (how_many_to_connect - 1)):
			win = True
			for i in range(how_many_to_connect):
				if board[r + i][c + i] != piece:
					win = False
					break
			if win:
				return True

	for c in range(COL_COUNT - (how_many_to_connect - 1)):
		for r in range((how_many_to_connect - 1), ROW_COUNT):
			win = True
			for i in range(how_many_to_connect):
				if board[r - i][c + i] != piece:
					win = False
					break
			if win:
				return True


def inp():
	while True:
		try:
			a = int(input())
			if 0 < a <= COL_COUNT:
				return a
		except:
			pass


def getRow(col):
	for y in range(ROW_COUNT):
		if board[y][col]:
			return y - 1
		if y == ROW_COUNT - 1:
			return ROW_COUNT - 1


def drop(col, turn):
	row = getRow(col)
	if row:
		board[row][col] = turn


def loop():
	turn = 0
	gameOver = False
	while not gameOver:
		printBoard()
		print("Player {}'s turn: ".format(turn + 1))
		turn = not turn
		col = inp() - 1
		drop(col, turn + 1)
		if winning_move(turn + 1):
			printBoard()
			print("Player {} has won".format(turn + 1))
			return


if __name__ == '__main__':
	loop()
	input('Press enter to continue...')
