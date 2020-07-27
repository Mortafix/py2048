from functools import reduce
from random import choice,random
import sys,tty,termios
from math import log2
from time import sleep

MOVESET = {'\x1b[A':'UP','\x1b[B':'DOWN','\x1b[C':'RIGHT','\x1b[D':'LEFT'}
BOARD = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
VALUE = [50,30,15,5,-10,20,10,5,0,0,0,0,0,0,0,0]
COLORS = ['148','226','208','196','199','207','128','057','021','045','036','028','010']
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
ENDC = '\033[0m'
ERASE = '\x1b[1A\x1b[2K'

class _Getch:
	def __call__(self):
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(3)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

def score_board(): return sum([2**n for n in BOARD if n])

def value_board(board): return sum([board[i]*VALUE[i] for i in range(16)]) if board else -1

def spawn_random(board): 
	try: board[choice([i for i in range(16) if board[i] == 0])] = 2 if random() > 0.9 else 1
	except IndexError: return board

def move_line(l,direction): return reduce(lambda x,y: x[:-1]+[y+1] if x[-1] == y else x+[y],[e for e in l[::direction] if e],[0])[1:][::direction]

def perform_move(board,move):
	direction = (-1,1)[move in ('LEFT','UP')]
	board = (board,[board[i*4+j] for j in range(4) for i in range(4)])[move in ('UP','DOWN')]
	result = reduce(lambda x,y:x+y if direction > 0 else x+y,[x+[0]*(4-len(x)) if direction > 0 else [0]*(4-len(x))+x for x in [move_line(board[i*4:i*4+4],direction) for i in range(4)]])
	new_board =(result,[result[i*4+j] for j in range(4) for i in range(4)])[move in ('UP','DOWN')]
	spawn_random(new_board)
	return new_board

def best_move(board,depth=1):
	if depth == 4: return max([value_board(valid_move(board,move)) for move in ['UP','DOWN','RIGHT','LEFT']])
	return max([(best_move(perform_move(board,move),depth+1),move) for move in ['UP','DOWN','RIGHT','LEFT']])[1]

def valid_move(board,move):
	next_board = perform_move(board,move)
	return next_board if next_board != BOARD else None

def cell_number(n):
	if n == 0: return f'\033[38;5;120m     {ENDC}'
	return f'\033[38;5;{COLORS[n%13]}m{2**n}{ENDC}'

def cancel_board(): print(ERASE*12)

def print_board():
	hline = BOLD+'-'*30+ENDC
	print(hline)
	print( '\n'.join(['{}\n{}'.format((' '+BOLD+'|'+ENDC+' ').join(['{:<20}'.format(cell_number(cell)) for cell in BOARD[i*4:i*4+4]]),hline) for i in range(4)]) )

if __name__ == '__main__':
	inkey = _Getch()
	POINTS = 0
	for _ in range(2): spawn_random(BOARD)
	try:
		while True:
			# print
			print(f'{UNDERLINE}Points{ENDC} \033[38;5;150m{score_board()}{ENDC}\n')
			print_board()
			# key input
			#inp = inkey()
			# perform move
			#print(best_move())
			#if is_valid_move(MOVESET.get(inp)):
			BOARD = perform_move(BOARD,best_move(BOARD))
			#spawn_random()
			#sleep(2)
			cancel_board()
	except ValueError: print('Game Over.')