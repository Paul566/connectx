import numpy as np
import random
import time


class Node:
    def __init__(self, grid, mark_to_move, num_rows, num_columns, inarow, my_mark, parameters=[2, 4, 0.5, 1, 2, 1.5, 1.],
                 verticals=None, horizontals=None, positive_diagonals=None, negative_diagonals=None):
        self.grid = grid.copy()
        self.mark_to_move = mark_to_move  # mark of the player to move
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.inarow = inarow  # number of marks in a row to win the game
        self.my_mark = my_mark
        self.parameters = parameters  # coefificents for the evaluation function
        self.verticals = verticals
        self.horizontals = horizontals
        self.positive_diagonals = positive_diagonals
        self.negative_diagonals = negative_diagonals
        
        self.found_lines = True
        if (self.verticals is None) or (self.horizontals is None) or (self.positive_diagonals is None) or (self.negative_diagonals is None):
            self.found_lines = False
        
    def get_verticals(self):
        # returns two lists of [r, c, m, n],
        # where r, c are coordinates of top points of vertical potential lines,
        # m is mark present in the potential line,
        # n is number of marks in the potential line (other squares are empty)\
        
        self.verticals = []
        
        for col in range(self.num_columns):
            num_ones = 0
            num_twos = 0
            for row in range(self.inarow):
                if self.grid[row][col] == 1:
                    num_ones += 1
                if self.grid[row][col] == 2:
                    num_twos += 1
                    
            for row in range(self.num_rows - self.inarow + 1):
                if num_ones == 0 and num_twos != 0:
                    self.verticals.append([row, col, 2, num_twos])
                if num_ones != 0 and num_twos == 0:
                    self.verticals.append([row, col, 1, num_ones])
                
                if row + self.inarow < self.num_rows:
                    if self.grid[row][col] == 1:
                        num_ones -= 1
                    if self.grid[row][col] == 2:
                        num_twos -= 1
                    
                    if self.grid[row + self.inarow][col] == 1:
                        num_ones += 1
                    if self.grid[row + self.inarow][col] == 2:
                        num_twos += 1
            
    def get_horizontals(self):
        # returns two lists of [r, c, m, n],
        # where r, c are coordinates of left points of horizontal potential lines,
        # m is mark present in the potential line,
        # n is number of marks in the potential line (other squares are empty)\
        
        self.horizontals = []
        
        for row in range(self.num_rows):
            num_ones = 0
            num_twos = 0
            for col in range(self.inarow):
                if self.grid[row][col] == 1:
                    num_ones += 1
                if self.grid[row][col] == 2:
                    num_twos += 1
                    
            for col in range(self.num_columns - self.inarow + 1):
                if num_ones == 0 and num_twos != 0:
                    self.horizontals.append([row, col, 2, num_twos])
                if num_ones != 0 and num_twos == 0:
                    self.horizontals.append([row, col, 1, num_ones])
                
                if col + self.inarow < self.num_columns:
                    if self.grid[row][col] == 1:
                        num_ones -= 1
                    if self.grid[row][col] == 2:
                        num_twos -= 1
                    
                    if self.grid[row][col + self.inarow] == 1:
                        num_ones += 1
                    if self.grid[row][col + self.inarow] == 2:
                        num_twos += 1
            
    def get_positive_diagonals(self):
        # returns two lists of [r, c, m, n],
        # where r, c are coordinates of top-left points of diagonal potential lines,
        # m is mark present in the potential line,
        # n is number of marks in the potential line (other squares are empty)
        
        self.positive_diagonals = []
        diagonal_number = 0 - self.num_columns + self.inarow  # row - column
        
        while diagonal_number <= self.num_rows - self.inarow - 0:
            num_ones = 0
            num_twos = 0
            
            init_row = 0
            init_col = 0
            if diagonal_number > 0:
                init_row = diagonal_number
            if diagonal_number < 0:
                init_col = - diagonal_number
            
            for i in range(self.inarow):
                if self.grid[init_row + i][init_col + i] == 1:
                    num_ones += 1
                if self.grid[init_row + i][init_col + i] == 2:
                    num_twos += 1
                    
            if num_ones == 0 and num_twos != 0:
                self.positive_diagonals.append([init_row, init_col, 2, num_twos])
            if num_ones != 0 and num_twos == 0:
                self.positive_diagonals.append([init_row, init_col, 1, num_ones])
                    
            i = 0
            while init_row + i + self.inarow < self.num_rows and init_col + i + self.inarow < self.num_columns:
                if self.grid[init_row + i][init_col + i] == 1:
                    num_ones -= 1
                if self.grid[init_row + i][init_col + i] == 2:
                    num_twos -= 1

                if self.grid[init_row + i + self.inarow][init_col + i + self.inarow] == 1:
                    num_ones += 1
                if self.grid[init_row + i + self.inarow][init_col + i + self.inarow] == 2:
                    num_twos += 1
                    
                i += 1
                
                if num_ones == 0 and num_twos != 0:
                    self.positive_diagonals.append([init_row + i, init_col + i, 2, num_twos])
                if num_ones != 0 and num_twos == 0:
                    self.positive_diagonals.append([init_row + i, init_col + i, 1, num_ones])
                            
            diagonal_number += 1
                
    def get_negative_diagonals(self):
        # returns two lists of [r, c, m, n],
        # where r, c are coordinates of top-right points of diagonal potential lines,
        # m is mark present in the potential line,
        # n is number of marks in the potential line (other squares are empty)
        
        self.negative_diagonals = []
        diagonal_number = self.inarow - 1  # row + column
        
        while diagonal_number <= self.num_rows - self.inarow + self.num_columns - 1:
            num_ones = 0
            num_twos = 0
            
            init_row = 0
            init_col = self.num_columns - 1
            if diagonal_number < self.num_columns - 1:
                init_col = diagonal_number
            if diagonal_number > self.num_columns - 1:
                init_row = diagonal_number - self.num_columns + 1
            
            for i in range(self.inarow):
                if self.grid[init_row + i][init_col - i] == 1:
                    num_ones += 1
                if self.grid[init_row + i][init_col - i] == 2:
                    num_twos += 1
                    
            if num_ones == 0 and num_twos != 0:
                self.negative_diagonals.append([init_row, init_col, 2, num_twos])
            if num_ones != 0 and num_twos == 0:
                self.negative_diagonals.append([init_row, init_col, 1, num_ones])
                    
            i = 0
            while init_row + i + self.inarow < self.num_rows and init_col - i - self.inarow >= 0:
                if self.grid[init_row + i][init_col - i] == 1:
                    num_ones -= 1
                if self.grid[init_row + i][init_col - i] == 2:
                    num_twos -= 1

                if self.grid[init_row + i + self.inarow][init_col - i - self.inarow] == 1:
                    num_ones += 1
                if self.grid[init_row + i + self.inarow][init_col - i - self.inarow] == 2:
                    num_twos += 1
                    
                i += 1
                
                if num_ones == 0 and num_twos != 0:
                    self.negative_diagonals.append([init_row + i, init_col - i, 2, num_twos])
                if num_ones != 0 and num_twos == 0:
                    self.negative_diagonals.append([init_row + i, init_col - i, 1, num_ones])
                            
            diagonal_number += 1
        
    def get_lines(self):
        self.get_verticals()
        self.get_horizontals()
        self.get_positive_diagonals()
        self.get_negative_diagonals()
        self.found_lines = True
                    
    def evaluate(self):
        # assuming self.inarow is 4
        """
        ones_reward = 1
        twos_reward = 2
        threes_reward = 4
        vertical_ones_reward = 0.5  # vertical lines are easier to block
        vertical_twos_reward = 1
        vertical_threes_reward = 2
        large_row_reward = 1.5  # the lower the line is, the better
        intersection_reward = 1.  # if two lines intersect, it is a potential 'fork'
        """
        ones_reward = 1
        twos_reward, threes_reward, vertical_ones_reward, vertical_twos_reward, vertical_threes_reward, large_row_reward, intersection_reward = self.parameters
        
        if not self.found_lines:
            self.get_lines()
            
        evaluation = 0.
        
        for line in self.horizontals + self.positive_diagonals + self.negative_diagonals:
            multiplier = 1
            if line[2] != self.my_mark:
                multiplier = -1
                
            if line[3] == 1:
                evaluation += multiplier * ones_reward * (1. + large_row_reward * line[0] / self.num_rows)
            if line[3] == 2:
                evaluation += multiplier * twos_reward * (1. + large_row_reward * line[0] / self.num_rows)
            if line[3] == 3:
                evaluation += multiplier * threes_reward * (1. + large_row_reward * line[0] / self.num_rows)
            if line[3] == self.inarow:
                evaluation += multiplier * np.Inf
                
        for line in self.verticals:
            multiplier = 1
            if line[2] != self.my_mark:
                multiplier = -1
                
            if line[3] == 1:
                evaluation += multiplier * vertical_ones_reward
            if line[3] == 2:
                evaluation += multiplier * vertical_twos_reward
            if line[3] == 3:
                evaluation += multiplier * vertical_threes_reward
            if line[3] == self.inarow:
                evaluation += multiplier * np.Inf
                
        long_verticals = [x.copy() for x in self.verticals if x[3] >= 2]
        long_horizontals = [x.copy() for x in self.horizontals if x[3] >= 2]
        long_positive_diagonals = [x.copy() for x in self.positive_diagonals if x[3] >= 2]
        long_negative_diagonals = [x.copy() for x in self.negative_diagonals if x[3] >= 2]
                
        for v in long_verticals:
            multiplier = 1
            if v[2] != self.my_mark:
                multiplier = -1
                    
            for h in long_horizontals:
                if v[2] != h[2]:
                    continue
                    
                if h[1] <= v[1] and h[1] + self.inarow > v[1] and v[0] <= h[0] and v[0] + self.inarow > h[0]:
                    evaluation += multiplier * v[3] * h[3] * intersection_reward
                    
                    # print("v-h", v, h, multiplier * v[3] * h[3] * intersection_reward)
                    
            for pd in long_positive_diagonals:
                if v[2] != pd[2]:
                    continue
                    
                intersection_row = pd[0] + v[1] - pd[1]
                intersection_col = v[1]
                    
                if (intersection_row >= v[0] and intersection_row < v[0] + self.inarow and 
                    intersection_row >= pd[0] and intersection_row < pd[0] + self.inarow):
                    evaluation += multiplier * v[3] * pd[3] * intersection_reward
                    
                    # print("v-pd", v, pd, multiplier * v[3] * pd[3] * intersection_reward)
                    
            for nd in long_negative_diagonals:
                if v[2] != nd[2]:
                    continue
                    
                intersection_row = nd[0] + nd[1] - v[1]
                intersection_col = v[1]
                    
                if (intersection_row >= v[0] and intersection_row < v[0] + self.inarow and 
                    intersection_row >= nd[0] and intersection_row < nd[0] + self.inarow):
                    evaluation += multiplier * v[3] * nd[3] * intersection_reward
                    
                    # print("v-nd", v, nd, multiplier * v[3] * nd[3] * intersection_reward)
                    
        for h in long_horizontals:
            multiplier = 1
            if h[2] != self.my_mark:
                multiplier = -1
                
            for pd in long_positive_diagonals:
                if h[2] != pd[2]:
                    continue
                
                intersection_row = h[0]
                intersection_col = pd[1] + h[0] - pd[0]
                
                if (intersection_col >= h[1] and intersection_col < h[1] + self.inarow and 
                    intersection_row >= pd[0] and intersection_row < pd[0] + self.inarow):
                    evaluation += multiplier * h[3] * pd[3] * intersection_reward
                    
                    # print("h-pd", h, pd, multiplier * h[3] * pd[3] * intersection_reward)
                    
            for nd in long_negative_diagonals:
                if h[2] != nd[2]:
                    continue
                
                intersection_row = h[0]
                intersection_col = nd[1] + nd[0] - h[0]
                
                if (intersection_col >= h[1] and intersection_col < h[1] + self.inarow and 
                    intersection_row >= nd[0] and intersection_row < nd[0] + self.inarow):
                    evaluation += multiplier * h[3] * nd[3] * intersection_reward
                    
                    # print("h-nd", h, nd, multiplier * h[3] * nd[3] * intersection_reward)
                    
        for pd in long_positive_diagonals:
            for nd in long_negative_diagonals:
                if pd[2] != nd[2]:
                    continue
                multiplier = 1
                if pd[2] != self.my_mark:
                    multiplier = -1
                    
                if (nd[0] + nd[1] - pd[0] - pd[1]) % 2 != 0:
                    continue
                
                intersection_row = pd[0] + (nd[0] + nd[1] - pd[0] - pd[1]) // 2
                intersection_col = pd[1] + (nd[0] + nd[1] - pd[0] - pd[1]) // 2
                
                if (intersection_row >= pd[0] and intersection_row < pd[0] + self.inarow and
                    intersection_row >= nd[0] and intersection_row < nd[0] + self.inarow):
                    evaluation += multiplier * pd[3] * nd[3] * intersection_reward
                    
                    # print(pd, nd, multiplier * pd[3] * nd[3] * intersection_reward)
        
        return evaluation
    
    def get_children(self):
        if self.is_terminal():
            return []
        
        children = []
        for col in range(self.num_columns):
            if self.grid[0][col] != 0:
                continue
                
            next_grid = self.grid.copy()
            next_verticals = []
            next_horizontals = []
            next_positive_diagonals = []
            next_negative_diagonals = []
            
            row = 0
            for potential_row in range(self.num_rows - 1, - 1, - 1):
                if next_grid[potential_row][col] == 0:
                    next_grid[potential_row][col] = self.mark_to_move
                    row = potential_row
                    break
                    
            for v in self.verticals:
                if v[0] <= row and v[0] + self.inarow > row and v[1] == col:
                    if v[2] == self.mark_to_move:
                        v_copy = v.copy()
                        v_copy[3] += 1
                        next_verticals.append(v_copy)
                    else:
                        continue
                else:
                    next_verticals.append(v.copy())
                    
            for h in self.horizontals:
                if h[1] <= col and h[1] + self.inarow > col and h[0] == row:
                    if h[2] == self.mark_to_move:
                        h_copy = h.copy()
                        h_copy[3] += 1
                        next_horizontals.append(h_copy)
                    else:
                        continue
                else:
                    next_horizontals.append(h.copy())
                    
            for pd in self.positive_diagonals:
                if pd[0] - pd[1] == row - col and pd[0] <= row and pd[0] + self.inarow > row:
                    if pd[2] == self.mark_to_move:
                        pd_copy = pd.copy()
                        pd_copy[3] += 1
                        next_positive_diagonals.append(pd_copy)
                    else:
                        continue
                else:
                    next_positive_diagonals.append(pd.copy())
                
            for nd in self.negative_diagonals:
                if nd[0] + nd[1] == row + col and nd[0] <= row and nd[0] + self.inarow > row:
                    if nd[2] == self.mark_to_move:
                        nd_copy = nd.copy()
                        nd_copy[3] += 1
                        next_negative_diagonals.append(nd_copy)
                    else:
                        continue
                else:
                    next_negative_diagonals.append(nd.copy())
            
            children.append(Node(next_grid, self.mark_to_move % 2 + 1, self.num_rows, self.num_columns, self.inarow, self.my_mark,
                                verticals=next_verticals, horizontals=next_horizontals, positive_diagonals=next_positive_diagonals,
                                negative_diagonals=next_negative_diagonals))
        
        return children
    
    def is_terminal(self):
        # Check for a tie
        if list(self.grid[0,:]).count(0)==0:
            return True
        
        if not self.found_lines:
            self.get_lines()
                    
        for line in self.verticals + self.horizontals + self.positive_diagonals + self.negative_diagonals:
            if line[3] == self.inarow:
                return True
        
        return False
        
        
        
class Minimax:
    def __init__(self, root, visit_nodes, silent=False):
        self.root = root
        self.valid_moves = root.get_children()
        self.depth = int(np.log(visit_nodes) / (np.log(len(self.valid_moves)) + 0.1))  # regularization in case there is one valid move
        self.nodes_visited = 0
        self.silent = silent
        self.opening_book = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,2,0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1,0,0,0,0,0,0,2,0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,2,0,0,0,0,0,0,1,0,0,0,0,0,0,2,0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,2,0,0,0,0,0,0,1,0,0,0,0,0,0,2,0,0,0,0,2,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,0,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,2,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,0,1,2],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,0,1,2,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,2,1,0,1,2],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,2,1,0,1,2,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1,0,0,0,2,1,0,1,2],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1,0,0,0,0,0,2,1,0,1,2,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,2,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,2,0,0]
        ]
        self.opening_answers = [(5, 3), (3, 3), (2, 3), (1, 3), (5, 1), (4, 1), (5, 5), (5, 1), (5, 6), (5, 0), (4, 5), (4, 1), (3, 5), (3, 1), (4, 3), (4, 3), (3, 2), (3, 4)]
        
    def minimax(self, node, depth, maximizing_player, alpha, beta):
        self.nodes_visited += 1
        valid_moves = node.get_children()
        
        if depth >= self.depth or (not valid_moves):
            return node.evaluate()
        
        if maximizing_player:
            value = - np.Inf
            for child in valid_moves:
                value = max(value, self.minimax(child, depth + 1, False, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = np.Inf
            for child in valid_moves:
                value = min(value, self.minimax(child, depth + 1, True, alpha, beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value
    
    def make_move(self):
        # returns a child of the root with best score
        start_time = time.time()
        
        # check opening book
        if list(self.root.grid.flatten()) in self.opening_book:
            row, col = self.opening_answers[self.opening_book.index(list(self.root.grid.flatten()))]
            next_grid = self.root.grid.copy()
            next_grid[row][col] = self.root.my_mark
            return Node(next_grid, self.root.mark_to_move % 2 + 1, self.root.num_rows, self.root.num_columns, self.root.inarow, self.root.my_mark)
        
        start_time = time.time()
        
        scores = {}
        depth_reduced = False
        for valid_move in self.valid_moves:
            scores[valid_move] = self.minimax(valid_move, 0, False, - np.Inf, np.Inf)
            now_time = time.time()
            if now_time - start_time > 1. and not depth_reduced:
                self.depth -= 2
                depth_reduced = True
            
        best_moves = [key for key in scores.keys() if scores[key] == max(scores.values())]
        next_move = random.choice(best_moves)
        
        if not self.silent:
            evaluation = max(scores.values())
            if self.root.my_mark == 2:
                evaluation = - evaluation
            end_time = time.time()
            print(f'time {end_time - start_time},\t visited {self.nodes_visited} nodes,\t eval {evaluation}')
            print(f'next move: {next_move.grid}')
        
        return next_move


def my_agent(obs, config):
    parameters = [2., 4., 2.93518357, 1., 2.58320125, 3.00020255, 3.23011953]    
    grid = np.asarray(obs.board).reshape(config.rows, config.columns)
    root = Node(grid, obs.mark, config.rows, config.columns, config.inarow, obs.mark, parameters)
    minimax = Minimax(root, 50000, silent=True)
    
    next_node = minimax.make_move()
    difference = next_node.grid - grid
    return int(np.where(difference == obs.mark)[1])
