import numpy as np


class Node:
    def __init__(self, grid, mark_to_move, num_rows, num_columns, inarow, my_mark):
        self.grid = grid.copy()
        self.mark_to_move = mark_to_move  # mark of the player to move
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.inarow = inarow  # number of marks in a row to win the game
        self.my_mark = my_mark
        
    def check_window(self, window, num_disc, piece):
        return (window.count(piece) == num_disc and window.count(0) == self.inarow - num_disc)
        
    def count_windows(self, num_disc, piece):
        num_windows = 0
        
        # Horizontal
        for row in range(self.num_rows):
            for col in range(self.num_columns - self.inarow + 1):
                window = list(self.grid[row, col:(col + self.inarow)])
                if self.check_window(window, num_disc, piece):
                    num_windows += 1
                
        # Vertical
        for col in range(self.num_columns):
            for row in range(self.num_rows - self.inarow + 1):
                window = list(self.grid[row:(row + self.inarow), col])
                if self.check_window(window, num_disc, piece):
                    num_windows += 1
                    
        # Positive Diagonal
        for row in range(self.num_rows - self.inarow + 1):
            for col in range(self.num_columns - self.inarow + 1):
                window = list(self.grid[range(row, row + self.inarow), range(col, col + self.inarow)])
                if self.check_window(window, num_disc, piece):
                    num_windows += 1
        
        #Negative Diagonal
        for row in range(self.inarow - 1, self.num_rows):
            for col in range(self.num_columns - self.inarow + 1):
                window = list(self.grid[range(row, row - self.inarow, - 1), range(col, col + self.inarow)])
                if self.check_window(window, num_disc, piece):
                    num_windows += 1
        
        return num_windows
        
    def evaluate(self):
        A = 1000000
        B = 2
        C = 1
        
        num_twos = self.count_windows(2, self.my_mark)
        num_threes = self.count_windows(3, self.my_mark)
        num_fours = self.count_windows(4, self.my_mark)
        
        num_twos_opp = self.count_windows(2, self.my_mark % 2 + 1)
        num_threes_opp = self.count_windows(3, self.my_mark % 2 + 1)
        num_fours_opp = self.count_windows(4, self.my_mark % 2 + 1)
        
        """print(self.grid)
        print(num_twos, num_threes, num_fours)
        print(num_twos_opp, num_threes_opp, num_fours_opp)
        print(A * num_fours + B * num_threes + C * num_twos - C * num_twos_opp - B * num_threes_opp - A * num_fours_opp)"""
        
        return A * num_fours + B * num_threes + C * num_twos - C * num_twos_opp - B * num_threes_opp - A * num_fours_opp
    
    def get_children(self):
        if self.is_terminal():
            return []
        
        children = []
        for col in range(self.num_columns):
            if self.grid[0][col] != 0:
                continue
                
            next_grid = self.grid.copy()
            for row in range(self.num_rows - 1, - 1, - 1):
                if next_grid[row][col] == 0:
                    next_grid[row][col] = self.mark_to_move
                    break
            children.append(Node(next_grid, self.mark_to_move % 2 + 1, self.num_rows, self.num_columns, self.inarow, self.my_mark))
        
        return children
    
    def is_terminal_window(self, window):
        return window.count(1) == self.inarow or window.count(2) == self.inarow
    
    def is_terminal(self):
        # Check for a tie
        if list(self.grid[0,:]).count(0)==0:
            return True
        
        # Horizontal
        for row in range(self.num_rows):
            for col in range(self.num_columns - self.inarow + 1):
                window = list(self.grid[row, col:(col + self.inarow)])
                if self.is_terminal_window(window):
                    return True
                
        # Vertical
        for col in range(self.num_columns):
            for row in range(self.num_rows - self.inarow + 1):
                window = list(self.grid[row:(row + self.inarow), col])
                if self.is_terminal_window(window):
                    return True
                    
        # Positive Diagonal
        for row in range(self.num_rows - self.inarow + 1):
            for col in range(self.num_columns - self.inarow + 1):
                window = list(self.grid[range(row, row + self.inarow), range(col, col + self.inarow)])
                if self.is_terminal_window(window):
                    return True
        
        #Negative Diagonal
        for row in range(self.inarow - 1, self.num_rows):
            for col in range(self.num_columns - self.inarow + 1):
                window = list(self.grid[range(row, row - self.inarow, - 1), range(col, col + self.inarow)])
                if self.is_terminal_window(window):
                    return True
        
        return False
        