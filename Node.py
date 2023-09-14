import numpy as np
from bitboard_utils import *


class Node:
    def __init__(self, bitboard_occupied, bitboard_black, mark_to_move, num_rows, num_columns, inarow, my_mark, all_masks,
                lines_white=None, lines_black=None, evaluated_lines=False):
        self.bitboard_occupied = bitboard_occupied
        self.bitboard_black = bitboard_black
        self.mark_to_move = mark_to_move  # mark of the player to move
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.inarow = inarow  # number of marks in a row to win the game
        self.my_mark = my_mark
        self.all_masks = all_masks  # botboard masks for self.inarow squares in a row
        self.lines_white = lines_white  # lines_white[i] is the number of potential lines with i+1 white pieces, len(lines_white) is inarow
        self.lines_black = lines_black
        self.evaluated_lines = evaluated_lines
        
    def evaluate_lines(self):
        self.lines_white, self.lines_black = count_lines(self.bitboard_occupied, self.bitboard_black, self.all_masks, self.inarow)
        self.evaluated_lines = True
                    
    def evaluate(self):
        # assuming self.inarow is 4

        ones_reward = 1
        twos_reward, threes_reward = 2, 5
        
        if not self.evaluated_lines:
            self.evaluate_lines()
        
        multiplier = 1 if self.my_mark == 2 else -1
        
        if self.lines_white[3]:
            return multiplier * np.Inf
        if self.lines_black[3]:
            return - multiplier * np.Inf

        evaluation = multiplier * (self.lines_white[0] * ones_reward + self.lines_white[1] * twos_reward + 
                                   self.lines_white[2] * threes_reward - 
                                   self.lines_black[0] * ones_reward - self.lines_black[1] * twos_reward - 
                                   self.lines_black[2] * threes_reward)
        
        return evaluation
    
    def get_children(self):
        if self.is_terminal():
            return []
        
        children = []
        for col in range(self.num_columns):
            if self.bitboard_occupied & (1 << col):
                continue
                
            position = col
            while position + self.num_columns < self.num_rows * self.num_columns and not (self.bitboard_occupied & (1 << (position + self.num_columns))):
                position += self.num_columns
                
            next_bitboard_occupied = self.bitboard_occupied + (1 << position)
            next_bitboard_black = self.bitboard_black
            if self.mark_to_move == 2:
                next_bitboard_black += (1 << position)
                
            children.append(Node(next_bitboard_occupied, next_bitboard_black, self.mark_to_move % 2 + 1, self.num_rows, self.num_columns, self.inarow, self.my_mark, self.all_masks))
        
        return children
    
    def is_terminal(self):
        # Check for a tie
        if board_is_filled(self.bitboard_occupied, self.num_rows, self.num_columns):
            return True
                    
        if not self.evaluated_lines:
            self.evaluate_lines()
            
        return (self.lines_white[-1] or self.lines_black[-1])
        