## AI ##

import chess

def game_over(board):
	if board.is_checkmate():
		return True
	elif board.is_stalemate():
		return True
	elif board.is_insufficient_material():
		return True
	elif board.is_fivefold_repetition():
		return True
	elif board.is_seventyfive_moves():
		return True
	elif board.can_claim_draw():
		return True
	return False

def get_legal_moves(board):
	l_moves = str(board.legal_moves).split()
	if len(l_moves) > 3:
		for i in range(3):
			l_moves.pop(0)
		l_moves = str(l_moves).replace(",", "")
		l_moves = str(l_moves).replace("(", "")
		l_moves = str(l_moves).replace(">", "")
		l_moves = str(l_moves).replace(")", "")
		l_moves = str(l_moves).replace("[", "")
		l_moves = str(l_moves).replace("]", "")
		l_moves = str(l_moves).replace("'", "")
		l_moves = l_moves.split()
	else:
		l_moves = [""]
	return l_moves

def get_board_score(player, board):
	score = 0
	piece_score = 0
	if player == "white":
		piece_color = chess.WHITE
	else:
		piece_color = chess.BLACK
	
	for i in range(1, 6):
		piece_amount = len(board.pieces(i, piece_color))
		if i == 1:
			piece_score = piece_amount * 10
			score += piece_score
		elif i == 2:
			piece_score = piece_amount * 30 
			score += piece_score
		elif i == 3:
			piece_score = piece_amount * 30 
			score += piece_score
		elif i == 4:
			piece_score = piece_amount * 50 
			score += piece_score
		elif i == 5:
			piece_score = piece_amount * 90 
			score += piece_score
		else:
			piece_score = piece_amount * 900
			score += piece_score
	return score
			
def minimax(board, depth, player, alpha, beta):
	if depth == 0:
		return get_board_score(player, board)

	moves = get_legal_moves(board)
	moves_size = len(moves)
	
	if moves_size  == 0:
		if	board.is_checkmate():
			return -9999
		return 0
	
	if player ==  "black":
		best_score = -9999
	else:
		best_score = 9999 

	#maximizing
	if player == "black":
		for move in moves:
			board.push_san(move)
			new_score = -minimax(board, depth -1, player, alpha, beta)
			best_score = max(alpha, new_score)
			alpha = max(new_score, best_score)
			if beta <= alpha:
				board.pop()
				break
			board.pop()
	
	#minimizing
	else:
		for move in moves:
			board.push_san(move)
			new_score = minimax(board, depth -1, player, alpha, beta)
			best_score = min(beta, new_score)
			beta = min(beta, new_score)
			if beta <= alpha:
				board.pop()
				break
			board.pop()

	return best_score

def get_best_move(board, player):
	score = 0
	alpha = -9999
	beta = 9999
	print("\nThinking...")
	best_move = ""
	start_board = board
	legal_moves = get_legal_moves(board)
	if player == "white":
		best_score = -9999
	else:
		best_score = 9999 
	    
	for move in legal_moves:
		board.push_san(move)
		score = minimax(board, 3, player, alpha, beta)
		
		if player == "white":
			if best_score < score: 
				best_score = score
				best_move = move 		

		else:
			if best_score > score:
				best_score = score
				best_move = move 		
		board.pop()
		
	print(f"\nmove = {best_move}")
	return best_move 		
