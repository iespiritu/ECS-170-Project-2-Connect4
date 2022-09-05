
boardtest = [[0,0,1,0,0,0,0],
				 [0,0,2,0,2,1,1],
				 [1,0,1,0,2,2,1],
				 [2,1,1,0,1,1,2],
				 [2,2,1,1,2,2,1],
				 [1,1,2,1,2,2,1]]
topPosition = [1,2,-1,3,0,0,0]
def connectEval(board, topPosition, turnPlayer):
	player1connect = [0,0,0,0]
	player2connect = [0,0,0,0]
	evaluation_final = 0
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
					
			elif board[i][j] == temp and temp != 0: # Add to stack
				stack += 1
				if stack > 4 and j != 6: 
					if temp == 1: player1connect[3] += 1
					elif temp == 2: player2connect[3] += 1
					print("OOPSIE")
						
			temp = board[i][j]

		if temp == 1: player1connect[stack-1] += 1
		elif temp == 2: player2connect[stack-1] += 1 

	# print('after rows')
	# print(player1connect)
	# print(player2connect)
	

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

	# print('after main diag')
	# print(player1connect)
	# print(player2connect)

	
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

	# print('after rows')
	# print(player1connect)
	# print(player2connect)

	#check columns
	for column in range(7):
		row = topPosition[column]+1  #topPosition in other file
		if row > 2 or row == 0: continue
		currPlayer = board[row][column]
		connectLen = 1
		if board[row+1][column] == currPlayer:
			connectLen = 2
			if board[row+2][column] == currPlayer:
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

final_eval = connectEval(boardtest, topPosition, 2)
print (final_eval)


