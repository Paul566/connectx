import numpy as np
import random
from Node import Node


class Minimax:
    def __init__(self, root, depth):
        self.root = root
        self.depth = depth
        
    def minimax(self, node, depth, maximizing_player, alpha, beta):
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
        valid_moves = self.root.get_children()
        scores = dict(zip(valid_moves, [self.minimax(child, 0, False, - np.Inf, np.Inf) for child in valid_moves]))
        best_moves = [key for key in scores.keys() if scores[key] == max(scores.values())]
        
        """for key in scores:
            print(key.grid, key.count_windows(4, 1), key.count_windows(4, 2), key.evaluate())"""
        
        
        return random.choice(best_moves)
    