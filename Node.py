import numpy as np
from bitboard_utils import *


class Node:
    def __init__(self, bitboard_occupied, bitboard_black, mark_to_move, num_rows, num_columns, inarow, my_mark, all_masks,
                active_masks_white=None, active_masks_black=None):
        self.bitboard_occupied = bitboard_occupied
        self.bitboard_black = bitboard_black
        self.mark_to_move = mark_to_move  # mark of the player to move
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.inarow = inarow  # number of marks in a row to win the game
        self.my_mark = my_mark
        self.all_masks = all_masks  # bitboard masks for self.inarow squares in a row
        self.active_masks_white = active_masks_white
        self.active_masks_black = active_masks_black
        if active_masks_black is None or active_masks_white is None:
            self.active_masks_white, self.active_masks_black = get_active_masks(self.bitboard_occupied, self.bitboard_black, self.all_masks)
              
    def evaluate(self):
        # assuming self.inarow is 4

        ones_reward = 1
        twos_reward, threes_reward = 2, 5
        
        multiplier = 1 if self.my_mark == 1 else -1

        evaluation = 0.
        
        if len(self.active_masks_white > 0):
            for ww in (self.bitboard_occupied & ~ self.bitboard_black) & self.active_masks_white:
                num_marks = bin(ww).count("1")
                if num_marks == 1:
                    evaluation += multiplier * ones_reward
                if num_marks == 2:
                    evaluation += multiplier * twos_reward
                if num_marks == 3:
                    evaluation += multiplier * threes_reward
                if num_marks == self.inarow:
                    return multiplier * np.Inf
            
        if len(self.active_masks_black > 0):
            for bw in self.bitboard_black & self.active_masks_black:
                num_marks = bin(bw).count("1")
                if num_marks == 1:
                    evaluation -= multiplier * ones_reward
                if num_marks == 2:
                    evaluation -= multiplier * twos_reward
                if num_marks == 3:
                    evaluation -= multiplier * threes_reward
                if num_marks == self.inarow:
                    return - multiplier * np.Inf
        
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
            difference = 1 << position
                
            next_bitboard_occupied = self.bitboard_occupied + difference
            next_bitboard_black = self.bitboard_black
            if self.mark_to_move == 2:
                next_bitboard_black += difference
                
            next_active_white = []
            next_active_black = []
            for mask in self.active_masks_white:
                if not (mask & difference):
                    next_active_white.append(mask)
                elif self.mark_to_move == 1:
                    next_active_white.append(mask)
            for mask in self.active_masks_black:
                if not (mask & difference):
                    next_active_black.append(mask)
                elif self.mark_to_move == 2:
                    next_active_black.append(mask)
                    
            potential_masks = get_intersecting_masks(difference, self.num_rows, self.num_columns, self.all_masks)
            for mask in potential_masks:
                if bin(mask & difference).count('1') == 1:
                    if self.mark_to_move == 1:
                        next_active_white.append(mask)
                    else:
                        next_active_black.append(mask)
                
            children.append(Node(next_bitboard_occupied, next_bitboard_black, self.mark_to_move % 2 + 1, self.num_rows, self.num_columns, 
                                 self.inarow, self.my_mark, self.all_masks, 
                                 active_masks_white=np.array(next_active_white), active_masks_black=np.array(next_active_black)))
        
        return children
    
    def is_terminal(self):
        # Check for a tie
        if board_is_filled(self.bitboard_occupied, self.num_rows, self.num_columns):
            return True
        
        if len(self.active_masks_white > 0):
            for ww in (self.bitboard_occupied & ~ self.bitboard_black) & self.active_masks_white:
                if bin(ww).count("1") == self.inarow:
                    return True
            
        if len(self.active_masks_black > 0):
            for bw in self.bitboard_black & self.active_masks_black:
                if bin(bw).count("1") == self.inarow:
                    return True
            
        return False
        