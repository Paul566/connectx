import numpy as np


def list_to_bitboard(listboard):
    # bitboard starts at bottom-right corner of the board, goes right to left and bottom to top, "0...01" is one mark in the top-left corner
    bitboard_occupied = 0  # self.num_rows * self.num_columns bit number, 1 if the square is filled, 0 if empty
    bitboard_black = 0  # self.num_rows * self.num_columns bit number, 1 if black piece, else 0
    
    for i, square in enumerate(listboard): 
        if square != 0:
            bitboard_occupied |= (1 << i)
            if square == 2:
                bitboard_black |= (1 << i)
                
    return bitboard_occupied, bitboard_black

def bitboard_to_array(bitboard_occupied, bitboard_black, num_rows, num_columns):
    ans = np.zeros(num_rows * num_columns)
    for i in range(num_rows * num_columns):
        if (bitboard_occupied >> i) & 1:
            if (bitboard_black >> i) & 1 == 0:
                ans[i] = 1
            else:
                ans[i] = 2
    return ans.reshape((num_rows, num_columns))

def board_is_filled(bitboard_occupied, num_rows, num_columns):
    return bitboard_occupied == (1 << num_rows * num_columns) - 1 

def get_line_masks(num_rows, num_columns, inarow):
    # returns horizontal_masks, vertical_masks, positive_diagonal_masks, negative_diagonal_masks, which are
    # lists of bitboard masks of inarow 1's in lines in specific directions

    horizontal_masks = []
    vertical_masks = []
    positive_diagonal_masks = []
    negative_diagonal_masks = []

    horizontal_mask = 0
    vertical_mask = 0
    positive_diagonal_mask = 0
    negative_diagonal_mask = 0
    
    for i in range(inarow):
        horizontal_mask |= 1 << i
        vertical_mask |= 1 << i * num_columns
        positive_diagonal_mask |= 1 << i * num_columns + i
        negative_diagonal_mask |= 1 << i * num_columns - i + inarow - 1

    row_inner = num_rows - inarow
    col_inner = num_columns - inarow
    for row in range(num_rows):
        for col in range(num_columns):
            offset = col + row * num_columns
            if col <= col_inner:
                horizontal_masks.append(horizontal_mask << offset)
            if row <= row_inner:
                vertical_masks.append(vertical_mask << offset)
            if col <= col_inner and row <= row_inner:
                positive_diagonal_masks.append(positive_diagonal_mask << offset)
                negative_diagonal_masks.append(negative_diagonal_mask << offset)

    return np.array(horizontal_masks), np.array(vertical_masks), np.array(positive_diagonal_masks), np.array(negative_diagonal_masks)

def get_active_masks(bitboard_occupied, bitboard_black, masks):
    # returns (ans_white, ans_black), ans_white is the array of masks with some white pieces and no black pieces
        
    ans_white = []
    ans_black = []
    
    bitboard_white = bitboard_occupied & (~ bitboard_black)
    
    white_windows = bitboard_white & masks
    black_windows = bitboard_black & masks
            
    return masks[(black_windows == 0) & (white_windows != 0)], masks[(black_windows != 0) & (white_windows == 0)]

def get_intersecting_masks(difference, num_rows, num_columns, all_masks):
    """
    difference: a bitboard with one 1
    returns: all masks of length inarow that intersect difference
    """
    # TODO: optimize this
    intersections = all_masks & difference
    return all_masks[intersections != 0]
    