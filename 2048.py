from random import randint,random
import sys,tty,termios
from math import log2

moveset = {'\x1b[A':'UP','\x1b[B':'DOWN','\x1b[C':'RIGHT','\x1b[D':'LEFT'}
TEST_BOARD = [[2,4,8,16],[32,64,128,256],[512,1024,2048,4096],[8192,16384,32768,65536]]
BOARD = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
COLORS = ['','\033[38;5;226m','\033[38;5;208m','\033[38;5;196m','\033[38;5;199m','\033[38;5;207m','\033[38;5;128m','\033[38;5;057m','\033[38;5;021m','\033[38;5;045m','\033[38;5;036m','\033[38;5;028m','\033[38;5;010m']
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

def spawn_random():
	if all([all([e for e in line]) for line in BOARD]): return -1
	row,col = randint(0,len(BOARD)-1),randint(0,len(BOARD)-1)
	while BOARD[row][col] != 0:
		row,col = randint(0,len(BOARD)-1),randint(0,len(BOARD)-1)
	BOARD[row][col] = 4 if random() > 0.9 else 2 

def move_line(l):
	global POINTS
	no_zero = [e for e in l if e]
	for i in range(len(no_zero)):
		if i+1 < len(no_zero) and no_zero[i] == no_zero[i+1]:
			POINTS += no_zero[i+1]
			no_zero[i+1] *= 2
			no_zero = no_zero[:i] + no_zero[i+1:]
			i += 1
	return no_zero

def move(where):
	board = list(map(list, zip(*BOARD))) if where in ['UP','DOWN'] else BOARD
	direction = 1 if where in ['LEFT','UP'] else -1
	result = [(line+[0]*(len(BOARD)-len(line)))[::direction] for line in [move_line(line[::direction]) for line in board]]
	return list(map(list, zip(*result))) if where in ['UP','DOWN'] else result

def color_number(n):
	if n == 0: return '{}{}{}'.format(COLORS[1],'     ',ENDC)
	power2 = int(log2(n)%13) if n < 5000 else int(log2(n)%13) + 1
	return '{}{}{}'.format(COLORS[power2],n,ENDC)

def cancel_board():
	print(ERASE*12)

def print_board():
	hline = BOLD+'-'*30+ENDC
	print(hline)
	print( '\n'.join(['{}\n{}'.format((' '+BOLD+'|'+ENDC+' ').join(['{:<20}'.format(color_number(cell)) for cell in line]),hline) for line in BOARD]) )

if __name__ == '__main__':
	inkey = _Getch()
	global POINTS
	POINTS = 0
	for _ in range(3): spawn_random()
	while True:
		cancel_board()
		print('{2}Points{3} {1}{0}{3}\n'.format(POINTS,'\033[38;5;150m',UNDERLINE,ENDC))
		print_board()
		inp = inkey()
		BOARD = move(moveset.get(inp)) if moveset.get(inp) else exit(-1)
		spawn_random()