import numpy as np
import random
import time
from Node import Node


class Minimax:
    def __init__(self, root, visit_nodes, silent=False):
        self.root = root
        self.valid_moves = root.get_children()
        self.depth = int(np.log(visit_nodes) / (np.log(len(self.valid_moves)) + 0.1))  # regularization in case there is one valid move
        self.nodes_visited = 0
        self.silent = silent
        
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
        
        # HEURISTIC: if the board is empty, put the mark in the middle
        if np.count_nonzero(self.root.grid) == 0:
            next_grid = self.root.grid.copy()
            next_grid[-1][self.root.num_columns // 2] = self.root.my_mark
            return Node(next_grid, self.root.mark_to_move % 2 + 1, self.root.num_rows, self.root.num_columns, self.root.inarow, self.root.my_mark)
        
        start_time = time.time()
        scores = dict(zip(self.valid_moves, [self.minimax(child, 0, False, - np.Inf, np.Inf) for child in self.valid_moves]))
        best_moves = [key for key in scores.keys() if scores[key] == max(scores.values())]
        
        if not self.silent:
            evaluation = max(scores.values())
            if self.root.my_mark == 2:
                evaluation = - evaluation
            end_time = time.time()
            print(f'time {end_time - start_time}, visited {self.nodes_visited} nodes, eval {evaluation}')
        
        return random.choice(best_moves)
    