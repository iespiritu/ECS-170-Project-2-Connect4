import random
import time
import pygame
import math
from copy import deepcopy
import numpy

weights =  [[3, 4,  5,  7,  5, 4, 3],
			[4, 6,  8, 10,  8, 6, 4], 
			[5, 8, 11, 13, 11, 8, 5],
			[5, 8, 11, 13, 11, 8, 5], 
			[4, 6,  8, 10,  8, 6, 4], 
			[3, 4,  5,  7,  5, 4, 3]]

class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):
	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):

	def play(self, env, move):
		board = deepcopy(env.board)
		self.topPosition = deepcopy(env.topPosition)
		print("topos ", self.topPosition)
		self.stack = [(-1,-1)]
		bestValue = -1024
		for nextMove in range(7):
			if self.playMove(board, nextMove, self.position):
				value = self.Min(board, 4)
				if value > bestValue:
					move[0] = nextMove
					bestValue = value
				self.undoMove(board)
		print("move ", move[0])
		print("value ", bestValue)
		return

	def Max(self, state, depth):
		if depth == 0:
			value = stupidEval(state, self.position)
			return value		
		value = -1024
		# if gameOver(state):
		# 	return value

		for nextMove in range(7):
			if self.playMove(state, nextMove, self.position):
				value = max(value, self.Min(state, depth - 1))
				self.undoMove(state)
				# print(self.stack)
		return value

	def Min(self, state, depth):
		if depth == 0:
			value = stupidEval(state, self.position)
			# print(value) 
			return value
		value = 1024
		# if gameOver(state):
		# 	return value

		for nextMove in range(7):
			if self.playMove(state, nextMove, self.opponent.position):
				value = min(value, self.Max(state, depth - 1))
				self.undoMove(state)
		return value

	def playMove(self, state, move, player):
		row = self.topPosition[move]
		if row == -1:
			return False
		state[row][move] = player
		self.stack.append(tuple((row, move)))
		self.topPosition[move] -= 1
		return True

	def undoMove(self, board):
		lastMove = self.stack.pop()
		self.topPosition[lastMove[1]] += 1
		board[lastMove] = 0
		return

class alphaBetaAI(connect4Player):

	def play(self, env, move):
		#copy stuff from game state so that its not mutated
		board = deepcopy(env.board)
		self.topPosition = deepcopy(env.topPosition)
		# print("topos ", self.topPosition)
		# variables for tree search
		self.stack = [(-1,-1)] 	# keeps track of move history
		# self.prune = 0 			# num of leaf nodes pruned
		self.gameOver = False
		# variables for alpha beta minimax
		bestValue = -1024
		bestMove = -1
		alpha = -1024
		beta = 1024
		# lists for sorted iterative deepening
		prevResults = [(3,0), (2,0), (4,0), (1,0), (5,0), (0,0), (6,0)]
		currResults = [(3,0)]
		movesLeft = sum(self.topPosition) + 7
		#check for immediate win
		for nextMove in range(7):
			if self.playMove(board, nextMove, self.position):
				self.undoMove(board)
			elif self.gameOver:
				move[0] = nextMove
				return
		# iterative deepening alpha-beta search
		for depth in range(2,movesLeft,1):
			#reset variables
			self.stack = [(-1,-1)]
			self.prune = 0
			self.gameOver = False
			bestValue = -1024
			bestMove = -1
			alpha = -1024
			beta = 1024
			currResults.clear()
			#top level Max function
			for nextMove in prevResults:
				if self.playMove(board, nextMove[0], self.position):
					value = self.Min(board, depth, alpha, beta)
					if value > bestValue:
						bestMove = nextMove[0]
						bestValue = value
					alpha = max(value, alpha)
					currResults.append(tuple((nextMove[0],value)))
					self.undoMove(board)
			#store results
			if bestMove != -1: 
				move[0] = bestMove
			# print(prevResults)
			prevResults = deepcopy(currResults)
			prevResults.sort(reverse = True, key = lambda x: x[1])
			# print("depth", depth)
			# print("move", move[0])
			# print("value", bestValue)
			# print("num prunes", self.prune)
			# print(currResults)
		print("achieved full depth!!")
		# for depth in range(3,10,1):
		# 	self.stack = [(-1,-1)]
		# 	self.prune = 0
		# 	self.gameOver = False
		# 	bestValue = -1024
		# 	bestMove = 3
		# 	alpha = -1024
		# 	beta = 1024
		# 	for nextMove in [3,2,4,1,5,0,6]:
		# 		if self.playMove(board, nextMove, self.position):
		# 			value = self.Min(board, depth, alpha, beta)
		# 			if value > bestValue:
		# 				bestMove = nextMove
		# 				bestValue = value
		# 			alpha = max(value, alpha)
		# 			self.undoMove(board)
		# 	move[0] = bestMove

		return

	def Max(self, state, depth, alpha, beta):
		if depth == 0:
			value = connectEval(state, self.topPosition, self.position)
			return value		
		value = -1024
		depth -= 1
		for nextMove in range(7):
			if self.playMove(state, nextMove, self.position):
				value = max(value, self.Min(state, depth, alpha, beta))
				alpha = max(value, alpha)
				self.undoMove(state)
				if value >= beta:
					break
					# self.prune += (6-nextMove)*(7**depth)
					# print("prune at max ", depth, alpha, beta, value)
				# print(self.stack)
			elif self.gameOver:
				self.gameOver = False
				return 1024
		return value

	def Min(self, state, depth, alpha, beta):
		if depth == 0:
			value = connectEval(state, self.topPosition, self.position)
			# print(value) 
			return value
		value = 1024
		depth -= 1
		for nextMove in range(7):
			if self.playMove(state, nextMove, self.opponent.position):
				value = min(value, self.Max(state, depth, alpha, beta))
				beta  = min(value, beta)
				self.undoMove(state)
				if value <= alpha:
					break
					# self.prune += (6-nextMove)*(7**depth)
					# print("prune at min ", depth, alpha, beta, value)
			elif self.gameOver:
				self.gameOver = False
				return -1024
		return value

	def playMove(self, state, move, player):
		row = self.topPosition[move]
		if row == -1:
			return False
		state[row][move] = player
		if testGameOver(state, row, move):
			self.gameOver = True
			state[row][move] = 0
			# print('game over with ', self.stack, row, move)
			return False

		self.stack.append(tuple((row, move)))
		self.topPosition[move] -= 1
		return True

	def undoMove(self, board):
		lastMove = self.stack.pop()
		self.topPosition[lastMove[1]] += 1
		board[lastMove] = 0
		return

testboard= [[0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0], 
			[2, 0, 0, 0, 0, 0, 0],
			[1, 1, 1, 0, 0, 0, 0], 
			[2, 1, 2, 0, 0, 0, 0], 
			[1, 2, 2, 1, 0, 0, 0]]

def testGameOver(board, row, column):
	player = board[row][column]
	#check column
	if row < 3:
		if board[row+1][column] == player and board[row+2][column] == player and board[row+3][column] == player:
			return True
	# check main diag
	if -4 < row-column and row-column <3:
		rowiter = row
		columniter = column
		connection = 1
		while rowiter >0 and columniter > 0:
			rowiter -= 1
			columniter -=1
			if board[rowiter][columniter] == player:
				connection +=1
			else:
				break
		if connection >=4:
			return True
		rowiter = row
		columniter = column
		while rowiter < 5 and columniter < 6:
			rowiter += 1
			columniter +=1
			if board[rowiter][columniter] == player:
				if connection >=3:
					return True
				connection += 1
			else:
				break
	# check inverse diag
	if 2 < row+column and row+column < 9: 
		rowiter = row
		columniter = column
		connection = 1
		while rowiter < 5 and columniter > 0:
			rowiter += 1
			columniter -=1
			if board[rowiter][columniter] == player:
				connection +=1
			else:
				break
		if connection >= 4:
			return True
		rowiter = row
		columniter = column
		while rowiter > 0 and columniter < 6:
			rowiter -= 1
			columniter +=1
			if board[rowiter][columniter] == player:
				if connection >= 3:
					return True
				connection += 1
			else:
				break
	# check row
	columniter = column
	connection = 1
	while columniter > 0:
		columniter -=1
		if board[row][columniter] == player:
			if connection >=3:
				return True
			connection +=1
		else:
			break
	columniter = column
	while columniter < 6:
		columniter +=1
		if board[row][columniter] == player:
			if connection >=3:
				return True
			connection += 1
		else:
			break
	return False

def stupidEval(board, topPosition, player):
	value = 0
	for i in range(0,6,1):
		for j in range(0,7,1):
			if board[i][j] == 1:
				value = value + weights[i][j]
			if board[i][j] == 2:
				value = value - weights[i][j]
	if player == 1: return value
	if player == 2: return -1*value

# print(weights)

# print(testGameOver(testboard, 3, 1))

def connectEval(board, topPosition, turnPlayer):
	player1connect = [0,0,0,0]
	player2connect = [0,0,0,0]
	evaluation_final = 0
	numTurns = 35 - sum(topPosition)
	if numTurns < 14:
		return stupidEval(board, topPosition, turnPlayer)
	# Horizontal check
	for i in range (6):
		temp = 0
		stack = 0
		for j in range (7):
			if board[i][j] != temp: #Stack must reset and values updated; temp tracks new player stack
				if temp == 1: player1connect[stack-1] += 1
				elif temp == 2: player2connect[stack-1] += 1
				if board[i][j] != 0: stack = 1
				else: stack = 0  
			elif temp != 0: # Add to stack
				stack += 1
			temp = board[i][j]

		if temp == 1: player1connect[stack-1] += 1
		elif temp == 2: player2connect[stack-1] += 1 
	#main diagnals
	for startPoint in [(2,0), (1,0), (0,0), (0,1), (0,2), (0,3)]:
		row = startPoint[0]
		column = startPoint[1]
		prevPlayer = 0
		connectLen = 0
		while row < 6 and column < 7:
			currPlayer = board[row][column]
			if currPlayer == 0 and prevPlayer == 0:
				pass
			elif currPlayer == prevPlayer or prevPlayer == 0:
				connectLen += 1
			else:
				if prevPlayer == 1: 
					player1connect[connectLen-1] +=1
				else:
					player2connect[connectLen-1] +=1
				if currPlayer == 0: 
					connectLen = 0
				else:
					connectLen = 1 
			row +=1
			column +=1
			prevPlayer = currPlayer
		if connectLen:
			if prevPlayer == 1: 
				player1connect[connectLen-1] +=1
			else:
				player2connect[connectLen-1] +=1 
	#reverse diagonals
	for startPoint in [(0,3), (0,4), (0,5), (0,6), (1,6), (2,6)]:
		row = startPoint[0]
		column = startPoint[1]
		prevPlayer = 0
		connectLen = 0
		while row < 6 and column >= 0:
			currPlayer = board[row][column]
			if currPlayer == 0 and prevPlayer == 0:
				pass
			elif currPlayer == prevPlayer or prevPlayer == 0:
				connectLen += 1
			else:
				if prevPlayer == 1: 
					player1connect[connectLen-1] +=1
				else:
					player2connect[connectLen-1] +=1
				if currPlayer == 0: 
					connectLen = 0
				else:
					connectLen = 1 
			row += 1
			column -= 1
			prevPlayer = currPlayer
		if connectLen:
			if prevPlayer == 1: 
				player1connect[connectLen-1] +=1
			else:
				player2connect[connectLen-1] +=1 
	#check columns
	for column in range(7):
		row = topPosition[column]+1  #topPosition in other file
		if row == 0 or row == 6: continue
		currPlayer = board[row][column]
		connectLen = 1
		if row < 5 and board[row+1][column] == currPlayer:
			connectLen = 2
			if row < 4 and board[row+2][column] == currPlayer:
				connectLen = 3
		if connectLen+row < 4: continue
		if currPlayer == 1: 
			player1connect[connectLen-1] +=1
		else:
			player2connect[connectLen-1] +=1 
	# print("Final values")
	# print("Player 1", player1connect)
	# print("Player 2", player2connect)
	evaluation_final = player1connect[0] + 8*player1connect[1] + 27*player1connect[2] - player2connect[0] - 8*player2connect[1] - 27*player2connect[2]
	if turnPlayer == 2: 
		evaluation_final *= -1
	return evaluation_final


# SQUARESIZE = 100
# BLUE = (0,0,255)
# BLACK = (0,0,0)
# RED = (255,0,0)
# YELLOW = (255,255,0)

# ROW_COUNT = 6
# COLUMN_COUNT = 7

# pygame.init()

# SQUARESIZE = 100

# width = COLUMN_COUNT * SQUARESIZE
# height = (ROW_COUNT+1) * SQUARESIZE

# size = (width, height)

# RADIUS = int(SQUARESIZE/2 - 5)

# screen = pygame.display.set_mode(size)



# print("eval test ", stupidEval(testboard))

'''
iterate columns
	iterate through items in column from bottom to top
		analzye as you go
		stop at a blank space
iterate rows
	iterate through items in row
		analyze as you go
iterate diagnols (left, then right)
	iterate through items in diagnals
		analyze as you go
'''