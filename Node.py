import numpy as np


class Node:
    def __init__(self, grid, mark_to_move, num_rows, num_columns, inarow, my_mark, 
                 verticals=None, horizontals=None, positive_diagonals=None, negative_diagonals=None):
        self.grid = grid.copy()
        self.mark_to_move = mark_to_move  # mark of the player to move
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.inarow = inarow  # number of marks in a row to win the game
        self.my_mark = my_mark
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
        A = 1000000
        B = 4
        C = 2
        D = 1
        
        if not self.found_lines:
            self.get_lines()
            
        evaluation = 0.
        
        for line in self.verticals + self.horizontals + self.positive_diagonals + self.negative_diagonals:
            multiplier = 1
            if line[2] != self.my_mark:
                multiplier = -1
                
            if line[3] == 1:
                evaluation += multiplier * D
            if line[3] == 2:
                evaluation += multiplier * C
            if line[3] == 3:
                evaluation += multiplier * B
            if line[3] == self.inarow:
                evaluation += multiplier * A
        
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
        