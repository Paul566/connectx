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
    