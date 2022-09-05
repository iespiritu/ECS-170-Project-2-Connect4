# ECS-170-Project-2-Connect4
Worked on a Connect4 AI for a group project in Intro to Artificial Intelligence

I devised two different evaluation functions to use to evaluate any state of the Connect4 board and return a value. Positive values favor player 1 whereas negative favor player 2. Minimax, Alpha Beta Pruning and Iterative Deepening would use this evaluation function to make a decision on what would be the best move for each player within a certain time limit. 

The first evaluation function uses assigned weights on every position of the board. 
 [[3, 4,  5,  7,  5, 4, 3],
  [4, 6,  8, 10,  8, 6, 4], 
  [5, 8, 11, 13, 11, 8, 5],
  [5, 8, 11, 13, 11, 8, 5], 
  [4, 6,  8, 10,  8, 6, 4], 
  [3, 4,  5,  7,  5, 4, 3]]
They are decided by the number of possible ways to make a connect4 at a particular position. Doing so favors weights in the center, so at the beginning stages of the game the AI would favor positions closer to the center. Evaluation returns the sum of the weights for each player and returns the difference. We decided the AI would use this evaluation for the first 14 moves.
evaluation = sum_player_1 - sum_player_2.

My job was to code the second evaluation function, which was to evaluate the number of 1's, 2's, and 3's in a row. 4's in a row and higher were negated because nodes in the branches of the AI's evaluation would be pruned or cut-off. Like the first evaluation, positive favors player 1 whereas negative favors player 2.
evaluation = player1_one + 4*player1_two + 8*player1_three - player2_one - 4*player2_two - 8*player2_three.
