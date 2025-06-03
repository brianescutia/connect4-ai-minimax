from cmath import inf
from copy import deepcopy
import random
import sys
import pygame
import numpy as np
import math
from connect4 import connect4

class connect4Player(object):
	def __init__(self, position, seed=0, CVDMode=False):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)
		if CVDMode:
			global P1COLOR
			global P2COLOR
			P1COLOR = (227, 60, 239)
			P2COLOR = (0, 255, 0)

	def play(self, env: connect4, move_dict: dict) -> None:
     
		move_dict["move"] = -1

class humanConsole(connect4Player):
	'''
	Human player where input is collected from the console
	'''
	def play(self, env: connect4, move_dict: dict) -> None:
		move_dict['move'] = int(input('Select next move: '))
		while True:
			if int(move_dict['move']) >= 0 and int(move_dict['move']) <= 6 and env.topPosition[int(move_dict['move'])] >= 0:
				break
			move_dict['move'] = int(input('Index invalid. Select next move: '))

class humanGUI(connect4Player):
	'''
	Human player where input is collected from the GUI
	'''

	def play(self, env: connect4, move_dict: dict) -> None:
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, P1COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, P2COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move_dict['move'] = col
					done = True

class randomAI(connect4Player):
	'''
	connect4Player that elects a random playable column as its move
	'''

	def play(self, env: connect4, move_dict: dict) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move_dict['move'] = random.choice(indices)

class stupidAI(connect4Player):
	'''
	connect4Player that will play the same strategy every time
	Tries to fill specific columns in a specific order 
	'''
	def play(self, env: connect4, move_dict: dict) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move_dict['move'] = 3
		elif 2 in indices:
			move_dict['move'] = 2
		elif 1 in indices:
			move_dict['move'] = 1
		elif 5 in indices:
			move_dict['move'] = 5
		elif 6 in indices:
			move_dict['move'] = 6
		else:
			move_dict['move'] = 0



class minimaxAI(connect4Player):
    # extended evaluation function for minimax AI
    def eval(self, env):
        output_dict = {}
        output_dict2 = {}
        #its going to evaluate the position by rows,columns, and diagonals
        # it will assign higher weights to longer sequences
        # count sequences in rows for self
        #count the number of 3's 2's and 1's 

        for i in range(6):
            count = 0
            
            for j in range(7):
                if env.board[i][j] == self.position:
                    count += 1 # count for consecutive pieces 
                else:
                    #update disctionary when sequence breaks
                    
                    
                    if count in output_dict and count != 0:
                        output_dict[count] += 1
                    elif count != 0:
                        output_dict[count] = 1
                    count = 0
                    
            if count in output_dict and count != 0:
                output_dict[count] += 1
            elif count != 0:
                output_dict[count] = 1
        
        # Count sequences in rows for opponent
        #it will be the same logic
        for i in range(6):
            count = 0
            for j in range(7):
                if env.board[i][j] == self.opponent.position:
                    count += 1
                else:
                    
                    
                    if count in output_dict2 and count != 0:
                        output_dict2[count] += 1
                    elif count != 0:
                        output_dict2[count] = 1
                    count = 0
                    
                    
            if count in output_dict2 and count != 0:
                output_dict2[count] += 1
            elif count != 0:
                output_dict2[count] = 1
        
        
        
        # Count sequences in columns for self
        for i in range(7):
            count = 0
            for j in range(6):
                if env.board[j][i] == self.position:
                    count += 1
                else:
                    if count in output_dict and count != 0:
                        output_dict[count] += 1
                    elif count != 0:
                        output_dict[count] = 1
                    count = 0
            if count in output_dict and count != 0:
                output_dict[count] += 1
            elif count != 0:
                output_dict[count] = 1
        
        
        # Count sequences in columns for opponent
        for i in range(7):
            count = 0
            for j in range(6):
                if env.board[j][i] == self.opponent.position:
                    count += 1
                else:
                    if count in output_dict2 and count != 0:
                        output_dict2[count] += 1
                    elif count != 0:
                        output_dict2[count] = 1
                    count = 0
            if count in output_dict2 and count != 0:
                output_dict2[count] += 1
            elif count != 0:
                output_dict2[count] = 1
        
        # Count sequences in diagonals (bottom left to top right) for self
        flipped_board = np.fliplr(env.board) # easier diagonal access
        for i in range(-2, 4):
            count = 0
            row = env.board.diagonal(i)
            
            
            for val in row:
                if val == self.position:
                    count += 1
                else:
                    
                    if count in output_dict and count != 0:
                        output_dict[count] += 1
                    elif count != 0:
                        output_dict[count] = 1
                    count = 0
            if count in output_dict and count != 0:
                output_dict[count] += 1
            elif count != 0:
                output_dict[count] = 1
        
           # Count sequences in diagonals (bottom left to top right) for opponent
        for i in range(-2, 4):
            count = 0
            row = flipped_board.diagonal(i)
            for val in row:
                if val == self.opponent.position:
                    count += 1
                else:
                    if count in output_dict2 and count != 0:
                        output_dict2[count] += 1
                    elif count != 0:
                        output_dict2[count] = 1
                    count = 0
            if count in output_dict2 and count != 0:
                output_dict2[count] += 1
            elif count != 0:
                output_dict2[count] = 1
        
        # Compute evaluation score
        self_result = 1 * output_dict.get(1, 0) + 5 * output_dict.get(2, 0) + 500 * output_dict.get(3, 0)
        
        opponent_result = 1 * output_dict2.get(1, 0) + 5 * output_dict2.get(2, 0) + 500 * output_dict2.get(3, 0)
        return self_result - opponent_result
    
    #simulate placing a piece to test moves
    def simulateMove(self, env, move, player):
        
        env.board[env.topPosition[move]][move] = player
        
        env.topPosition[move] -= 1
        env.history[0].append(move)
        return env
    
    def MAX(self, env, prev_move, depth):
        if env.gameOver(prev_move, self.opponent.position):
            return -inf
        
        if depth == 0:
            return self.eval(env)
        
        
        #this is the worst case 
        max_v = -inf
        possible = env.topPosition >= 0
        
        for i, move in enumerate(possible):
            if move:
                
                child = self.simulateMove(deepcopy(env), i, self.position)
                max_v = max(max_v, self.MIN(child, i, depth-1)) # Prune if alpha exceeds betaa
        return max_v
    
    def MIN(self, env, prev_move, depth):
        if env.gameOver(prev_move, self.position):
            return inf
        if depth == 0:
            return self.eval(env)
        
        min_v = inf
        possible = env.topPosition >= 0
        
        for i, move in enumerate(possible):
            
            if move:
                child = self.simulateMove(deepcopy(env), i, self.opponent.position)
                min_v = min(min_v, self.MAX(child, i, depth-1))
        return min_v
    
    def Minimax(self, env, move, max_depth):
        max_v = -inf
        possible = env.topPosition >= 0
        
        for i, next_move in enumerate(possible):
            
            
            if next_move:
                child = self.simulateMove(deepcopy(env), i, self.position)
                v = self.MIN(child, i , max_depth-1)
                
                if v > max_v:
                    max_v = v
                    move[0] = i
    
    def play(self, env, move):
        max_depth = 4
        self.Minimax(deepcopy(env), move, max_depth)
        print("Finished")


class alphaBetaAI(connect4Player):
    # Evaluation Function for alphaBetaAI
    def eval(self, env):
        output_dict = {}
        output_dict2 = {}

        # Count sequences in rows for self
        #count the number of 3's 2's and 1's 
        for i in range(6):
            
            count = 0
            for j in range(7):
                
                if env.board[i][j] == self.position:
                    count += 1
                    #update dictionary when sequence brekas
                else:
                    
                    if count in output_dict and count != 0:
                        output_dict[count] += 1
                    elif count != 0:
                        output_dict[count] = 1
                    count = 0
            if count in output_dict and count != 0:
                output_dict[count] += 1
            elif count != 0:
                output_dict[count] = 1

        # Count sequences in rows for opponent
        for i in range(6):
            count = 0
            for j in range(7):
                if env.board[i][j] == self.opponent.position:
                    count += 1
                else:
                    
                    if count in output_dict2 and count != 0:
                        output_dict2[count] += 1
                    elif count != 0:
                        output_dict2[count] = 1
                   
                    count = 0
            if count in output_dict2 and count != 0:
                output_dict2[count] += 1
                
            elif count != 0:
                output_dict2[count] = 1

        # Count sequences in columns for self
        for i in range(7):
            count = 0
            for j in range(6):
                if env.board[j][i] == self.position:
                    count += 1
                    
                else:
                    
                    if count in output_dict and count != 0:
                        output_dict[count] += 1
                    elif count != 0:
                        output_dict[count] = 1
                    count = 0
            if count in output_dict and count != 0:
                output_dict[count] += 1
            elif count != 0:
                output_dict[count] = 1

        # Count sequences in columns for opponent
        for i in range(7):
            count = 0
            for j in range(6):
                if env.board[j][i] == self.opponent.position:
                    count += 1
               
               
                else:
                    if count in output_dict2 and count != 0:
                        output_dict2[count] += 1
                    elif count != 0:
                        output_dict2[count] = 1
                    count = 0
            if count in output_dict2 and count != 0:
                output_dict2[count] += 1
            elif count != 0:
                output_dict2[count] = 1

        # Count sequences in diagonals for self
        
        # Counting sequences diagonally bottom left to top right for both players
        flipped_board = np.fliplr(env.board) 
        for i in range(-2, 4):
            count = 0
            row = env.board.diagonal(i)
            
            for val in row:
                if val == self.position:
                    count += 1
                    
                    
                else:
                    if count in output_dict and count != 0:
                        output_dict[count] += 1
                    elif count != 0:
                        output_dict[count] = 1
                    count = 0
            if count in output_dict and count != 0:
                output_dict[count] += 1
            elif count != 0:
                output_dict[count] = 1

        # Count sequences in diagonals for opponent
        for i in range(-2, 4):
            count = 0
            row = flipped_board.diagonal(i)
            for val in row:
                if val == self.opponent.position:
                    count += 1
                else:
                    if count in output_dict2 and count != 0:
                        output_dict2[count] += 1
                    elif count != 0:
                        output_dict2[count] = 1
                    count = 0
            if count in output_dict2 and count != 0:
                output_dict2[count] += 1
            elif count != 0:
                output_dict2[count] = 1

        # Compute evaluation score
        self_result = 1 * output_dict.get(1, 0) + 5 * output_dict.get(2, 0) + 500 * output_dict.get(3, 0)
        opponent_result = 1 * output_dict2.get(1, 0) + 5 * output_dict2.get(2, 0) + 500 * output_dict2.get(3, 0)
        
        return self_result - opponent_result
    
    #Simulate placing a piece to test moves 
    def simulateMove(self, env, move, player):
        
        env.board[env.topPosition[move]][move] = player
        env.topPosition[move] -= 1
        env.history[0].append(move)
        
        
        return env
    
    def MAX(self, env, prev_move, depth, alpha, beta):
        if env.gameOver(prev_move, self.opponent.position):
            return -inf
        if depth == 0:
            return self.eval(env)
        
        max_v = -inf
        possible = env.topPosition >= 0
        for i, move in enumerate(possible):
            
            if move:
                child = self.simulateMove(deepcopy(env), i, self.position)
                max_v = max(max_v, self.MIN(child, i, depth-1, alpha, beta))
                alpha = max(alpha, max_v)
                
                
                if max_v >= beta: # Pruning may occur
                    break
        return max_v
    
    def MIN(self, env, prev_move, depth, alpha, beta):
        if env.gameOver(prev_move, self.position):
            return inf
        if depth == 0:
            return self.eval(env)
        
        min_v = inf
        
        possible = env.topPosition >= 0
        for i, move in enumerate(possible):
            
            if move:
                child = self.simulateMove(deepcopy(env), i, self.opponent.position)
                min_v = min(min_v, self.MAX(child, i, depth-1, alpha, beta))
                beta = min(beta, min_v)
                if min_v <= alpha:
                    break
       
        return min_v
    #Pruning algorithm to find best move
    def AlphabetaPruning(self, env, move, max_depth, alpha, beta):
        max_v = -inf
        possible = env.topPosition >= 0
        
        
        for i, next_move in enumerate(possible):
            if next_move:
                child = self.simulateMove(deepcopy(env), i, self.position)
                v = self.MIN(child, i, max_depth-1, alpha, beta)
                if v > max_v:
                    max_v = v
                    move["move"] = i
    
    def play(self, env, move_dict):
        
        if len(env.history[0]) == 0:
            move_dict["move"] = 3

        alpha = -inf
        beta = inf
        max_depth = 4
        self.AlphabetaPruning(deepcopy(env), move_dict, max_depth, alpha, beta)
SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
P1COLOR = (255,0,0)
P2COLOR = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




