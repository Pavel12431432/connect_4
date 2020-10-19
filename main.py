import pygame

# define constants
how_many_to_connect = 4
COL_COUNT = 7
ROW_COUNT = 6
TILE_SIZE = 128
MAX_FPS = 144
FALLING_SPEED = 22
WIDTH, HEIGHT = COL_COUNT * TILE_SIZE, ROW_COUNT * TILE_SIZE

# pygame init
pygame.mixer.pre_init(44100, -16, 1, 4096)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Connect ' + str(how_many_to_connect))
pygame.display.set_icon(pygame.transform.scale(pygame.image.load('icon.png'), (32, 32)))
font = pygame.font.SysFont('impact', 120)
clock = pygame.time.Clock()

# import sounds
hit_sound = pygame.mixer.Sound('audio/hit.wav')
win_sound = pygame.mixer.Sound('audio/win.wav')
turn = 1

# import images
imgs = [
	pygame.transform.scale(pygame.image.load('sprites/empty.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)),
	pygame.transform.scale(pygame.image.load('sprites/red.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)),
	pygame.transform.scale(pygame.image.load('sprites/yellow.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)),
	pygame.transform.scale(pygame.image.load('sprites/selected.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))
]


class Piece:
	def __init__(self, img_index, goal, moving):
		self.img = img_index
		self.pos = 0
		self.goal = goal
		self.moving = moving

	def update(self):
		# update position
		self.pos = min(self.pos + FALLING_SPEED * self.moving, self.goal)
		# set moving to false if goal is met
		self.moving = not self.pos == self.goal


# place a piece on certain column
def place_piece(col_index, img_index):
	try:
		column = board[col_index]
		# find lowest open spot
		index = [len(column) - i - 1 for i in range(len(column[::-1])) if not column[::-1][i].img][0]
		# place piece
		board[col_index][index] = Piece(img_index, index * TILE_SIZE - 1, True)
		# play sound
		pygame.mixer.Sound.play(hit_sound)
		# return 1 if piece was placed
		return 1
	except (IndexError, TypeError):
		# return 0 if unable to place piece
		return 0


# draw board
def draw(mouse_pos):
	screen.fill((37, 37, 37))

	# draw each piece
	for col in range(len(board)):
		for piece in range(len(board[col])):
			p = board[col][piece]
			if p.img:
				# draw current piece
				screen.blit(imgs[p.img], (col * TILE_SIZE, p.pos))
				# update the current piece's position
				p.update()

	# draw grid
	for col in range(len(board)):
		for piece in range(len(board[col])):
			screen.blit(imgs[0], (col * TILE_SIZE, piece * TILE_SIZE))

	# draw selected space
	screen.blit(imgs[3], (mouse_pos[0] // TILE_SIZE * TILE_SIZE, mouse_pos[1] // TILE_SIZE * TILE_SIZE))

	pygame.display.update()


# check if game has ended
def winning_move(piece):
	# Check horizontal locations for win
	for c in range(COL_COUNT - (how_many_to_connect - 1)):
		for r in range(ROW_COUNT):
			if min([board[c + i][r].img == piece for i in range(how_many_to_connect)]):
				return True

	# Check vertical locations for win
	for c in range(COL_COUNT):
		for r in range(ROW_COUNT - (how_many_to_connect - 1)):
			if min([board[c][r + i].img == piece for i in range(how_many_to_connect)]):
				return True

	# Check \ diagonals
	for c in range(COL_COUNT - (how_many_to_connect - 1)):
		for r in range(ROW_COUNT - (how_many_to_connect - 1)):
			if min([board[c + i][r + i].img == piece for i in range(how_many_to_connect)]):
				return True

	# check / diagonals
	for c in range(COL_COUNT - (how_many_to_connect - 1)):
		for r in range((how_many_to_connect - 1), ROW_COUNT):
			if min([board[c + i][r - i].img == piece for i in range(how_many_to_connect)]):
				return True


# handle input
def inp():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
			return pygame.mouse.get_pos()[0] // TILE_SIZE


def end_game():
	# finish drawing falling pieces
	while True:
		# check if any piece is moving
		if max([max([board[col][piece].moving for piece in range(len(board[col]))]) for col in range(len(board))]):
			draw(pygame.mouse.get_pos())
		else:
			draw(pygame.mouse.get_pos())
			break
		inp()
		clock.tick(MAX_FPS)

	# show victory text
	text = font.render('Player {} has won!'.format(turn), True, (255, 255, 255))
	text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
	screen.blit(text, text_rect)
	pygame.display.update()

	# play win sound
	pygame.mixer.Sound.play(win_sound)

	while True:
		inp()


# init board
board = [[Piece(0, piece * TILE_SIZE, False) for col in range(ROW_COUNT)] for piece in range(COL_COUNT)]

# main loop
while True:
	# check if a piece has been placed
	if (i := inp()) != None and place_piece(i, turn):
		# check if a player has won
		if winning_move(turn):
			end_game()
		# change turn
		turn = 2 if turn == 1 else 1
	# draw board
	draw(pygame.mouse.get_pos())
	clock.tick(MAX_FPS)
