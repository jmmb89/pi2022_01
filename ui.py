## UI ##

import curses, os

opt = 0
menu_opts = ["1P", "2P", "HELP", "INFO"]
logo_pad = -10
p_help = False

logo_big = [\
"██████╗ ██╗   ██╗     ██████╗██╗  ██╗███████╗███████╗███████╗",\
"██╔══██╗╚██╗ ██╔╝    ██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝",\
"██████╔╝ ╚████╔╝     ██║     ███████║█████╗  ███████╗███████╗",\
"██╔═══╝   ╚██╔╝      ██║     ██╔══██║██╔══╝  ╚════██║╚════██║",\
"██║        ██║       ╚██████╗██║  ██║███████╗███████║███████║",\
"╚═╝        ╚═╝        ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝"]

logo_small=[\
" _____ __ __    _____ _____ _____ _____ _____ ",\
"|  _  |  |  |  |     |  |  |   __|   __|   __|",\
"|   __|_   _|  |   --|     |   __|__   |__   |",\
"|__|    |_|    |_____|__|__|_____|_____|_____|"]

t_help = [\
"H - Print this help",\
"Q or ESC - Exit program",\
"ARROW KEY - Move up or down",\
"ENTER - Select option"]

stdscr = curses.initscr()

def clear():
	#windows (nt)
	if os.name == "nt":
		os.system("cls")
	#UNIX (Posix)
	else:
		os.system("clear")

def key_down():
	global opt
	if opt == len(menu_opts) - 1:
		opt = 0
	else:
		opt += 1

def key_up():
	global opt
	if opt == 0:
		opt = len(menu_opts) - 1
	else:
		opt -= 1

def print_text(text, pad, job):
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

	h, w = stdscr.getmaxyx()
	for i in range(len(text)):
		x = w//2 - len(text[i])//2
		y = h//2 - len(text) + i + pad

		if job == "menu" and i == opt:
			stdscr.attron(curses.color_pair(1))
		stdscr.addstr(y, x, text[i])
		stdscr.attroff(curses.color_pair(1))
			
def print_menu():
	global p_help, logo, menu_opts, logo_pad, t_help

	stdscr.clear()
	h, w = stdscr.getmaxyx()
	#debug #os.system(f"echo {w} > log.txt")
	if w > 90 and h > 30:
		logo = logo_big
	elif w > 46 and h > 30:
		logo = logo_small
	else:
		logo  = ["PY CHESS"]

	print_text(logo, logo_pad, "logo")
	print_text(menu_opts, -2, "menu")

	if p_help:
		p_help = False
		print_text(t_help, -2, "help")

	stdscr.refresh()
		

def main(stdscr):
	global opt, p_help
	#hide cursor
	curses.curs_set(0)

	while True:
		print_menu()
		key = stdscr.getch()

		if key == curses.KEY_UP:
			key_up()
		elif key == curses.KEY_DOWN:
			key_down()
		elif key == 104: #h
			p_help = True
			print_menu()
		elif key == curses.KEY_ENTER or key in [10, 13]: #NL ou CR
			if opt == 2:
				p_help = True
			elif opt == 0 or opt == 1:
				break
		elif key == 113 or key == 27: #q or esc 
			opt = -1
			break

def main_menu():
	curses.wrapper(main)
	return opt
