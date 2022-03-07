###########################
#  PI A.I                 #
#                         #
#  PY CHESS               #
#  v1.01                  #
#                         #
###########################

import chess, os, sys, random
from ui import main_menu, clear 
from ai import get_best_move, get_legal_moves, game_over

# https://crivelaro.notion.site/Minimax-Engine-de-Xadrez-86f99816397145058f935890a1997b5e

debug = False 
whoplays = "white"
book_move = {}
key_list = []
move = ""

def is_player_turn(human):
	global whoplays
	if whoplays == "white":
		if human == "white":
			return True
		else:
			return False
	else:
		if human == "white":
			return False
		else:
			return True

def print_help():
	print("\nhelp  [h] - Show this help\
	\nquit  [q] - Close the program\
	\nclear [c] - Clear the screen\
	\nboard [b] - Print the board\
	\nlegal moves [lm] - Show legal moves\
	\n\nPlaying the game:\n\
	\ncomputer turn: play\
	\nplayer turn: play [move] or play (random move)\
	\n")

def can_make_move(board, move):
	try:
		move = board.parse_san(move)
		return move in board.legal_moves
	except:
		return False

def random_play(board):
	if debug:
		print("\nESCOLHEU RANDOM!")
	lm = get_legal_moves(board)
	move = random.choice(lm) 
	return move

def print_player_move(move):	
	global whoplays
	print(f"Human played move: {move}")
	print("\n#########################")
	if whoplays == "black":
		whoplays = "white"
	else:
		whoplays = "black"

def human_play(board, move, human, rand):
	global whoplays
	print("\nHUMAN PLAY:\n")
	if debug:
		print(f"input play: {move}")
	#se eh a vez do jogador
	if is_player_turn(human):
		#se a jogada eh valida
		if not rand:
			if can_make_move(board, move):
				board.push_san(move)
				print_player_move(move)
				return True
			else:
				print("INVALID MOVE!\n")
		else:
			move = random_play(board)
			board.push_san(move)
			print_player_move(move)
			return True
	else:
		print("NOT PLAYER TURN\n")
		
	return False

def computer_play(board, turn, human):
	global whoplays, book_move, key_list, move, debug
	computer = ""
	if human == "black":
		computer = "white"
		book_move  = {"pastor" : ["e2e4", "f1c4", "d1h5", "h5f7"], "ponziani" : ["e2e4", "g1f3","c2c3", "d2d4"]}
	else:
		### CRIAR MAIS JOGADAS / FAZER DEBUG DEPOIS ###
		computer = "black"
		book_move = {"Caro-kann exchange" : ["c7c6", "d7d5", "d7d5", "c8f5"]}

	if turn == 0:	
		key_list = [key for key in book_move]
		move = random.choice(key_list)	

	if debug:
		print(f"TURN = {turn}")
		print(f"LEN_BOOK_MOVE = {len(book_move[move])}")
	print("\nCOMPUTER PLAY:")
	if debug and turn < len(book_move[move]):
		print(f"\nstart strategy = {move}")
	if turn < len(book_move[move]) and can_make_move(board, book_move[move][turn]):
		print(f"play: {book_move[move][turn]}")
		board.push_san(book_move[move][turn])
	else:
		if human == "white":
			board.push_san(get_best_move(board,"black"))
		else:
			board.push_san(get_best_move(board,"white"))

	if whoplays == "black":
		whoplays = "white"
	else:
		whoplays = "black"
		
	return True
    
def end_game_status(board):
	print("done")

def print_legal_moves(moves):
	print("\nLegal Moves:\n")
	for move in moves:
			if move is not None: 
				print(move, end=" ")
	
def game(board, new_game, mode):
	human = ""
	turn = 0
	run_game = True
	show_board = True
	colors = ["white", "black"]

	if new_game:
		random.seed()
		human = random.choice(colors)
	else:
		human = input("\nSelect player color: [white, black]\n> ").lower()
		if human != "white" and human != "black":
			print("\nInvalid color, loading human as white..\n")
			human = "white"
	
	print(f"\n#####  {mode}  #####\n")
	print("\n# Enter help for info #\n")

	while run_game:
		if show_board:
			if is_player_turn(human):
				print(f"\nTURN: human\nCOLOR: {whoplays}\n")
			else:
				print(f"\nTURN: computer\nCOLOR: {whoplays}\n\n")
			print(board)
			show_board = False

		command = input("\nInsert Command:\n> ")
		command_array = command.split()
		
		if command == "q" or command == "quit" or command == "exit":
			run_game = False
			print("\nClosing the program..\nSee you later!\n")
		elif command == "help" or command == "h":
			print_help()
		elif command == "legal moves" or command == "lm":
			l_moves = get_legal_moves(board)
			#print(print_legal_moves(get_legal_moves(board)))
			print(f"Legal Moves: {l_moves}")
		elif command == "clear" or command == "c":
			clear()
			show_board = True
		elif len(command_array) > 0 and command_array[0] == "play":
			if not game_over(board):
				if len(command_array) > 1:
					show_board = human_play(board, command_array[1], human, False)
				else:
					if is_player_turn(human):
						show_board = human_play(board, "", human, True)
					else:	
						show_board = computer_play(board, turn, human)
						print("\n#########################")
						turn += 1
			else:
				end_game_status(board)
				print("\nClosing the program..\nSee you later!\n")
				run_game = False

		elif command == "b" or command == "board":
			show_board = True
		else:
			print("\nInvalid command! Enter help for info\n")
			
def game_init(): 
	option = main_menu()
	new_game = True
	board_status = ""

	if len(sys.argv) > 2:
		if sys.argv[1] == "-b":
			try:
				file = open(sys.argv[2], 'r')
				status = file.readlines()
				board_status = status[0]
				file.close()
			except:
				print(f"\nError, file {sys.argv[2]} dont exist")
		elif sys.argv[1] == "-s":
			board_status = sys.argv[2]
		else:
			print(f"\nUSAGE: python {sys.argv[0]} [-parameter] [file/string]")

	try:
		board = chess.Board(board_status)
		if option != -1:
			print("\nBoard loaded OK..")
			new_game = False
	except:
		board = chess.Board()
		if len(sys.argv) > 2:
			print("\nInvalid board format!\nLoading new game..")

	if option == -1:
		print("\nSee you later..\n")
	elif option == 0:
		game(board, new_game, "SINGLE PLAYER")
	elif option == 1:
		game(board, new_game, "MULTIPLAYER")

game_init()
