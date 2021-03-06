#!/bin/python3

import math
import os
import random
import re
import sys

# this can be done using bfs
# complexity O(m.n)


# Complete the minimumMoves function below.
from collections import deque

def next_pos(grid, row, col):
    # dirs thinking top, left, bottom, right
    dirrow = [-1, 0, 1, 0]
    dircol = [0, -1, 0, 1]

    for move_row, move_col in zip(dirrow, dircol):
        if (0 <= row + move_row < len(grid) and
            0 <= col + move_col < len(grid[0])):
            if grid[row + move_row][col + move_col] == '.':
                yield row + move_row, col + move_col


from pprint import pprint

def minimumMoves(grid, startX, startY, goalX, goalY):
    grid = [list(g) for g in grid]
    pprint(grid)
    row, col = startX, startY
    queue = deque([(row, col, 0)])
    visited = set([(row, col)])

    while queue:
        row, col, moves = queue.popleft()
        #print(row, col, moves, queue)
        if row == goalX and col == goalY:
            return moves

        for next_row_col in next_pos(grid, row, col):
            if next_row_col not in visited:
                visited.add((row, col))
                queue.append((*next_row_col, moves+1))
        #print(queue)

    return -1


print(minimumMoves(['.X.', '.X.', '...'], 0, 0, 0, 2))

grid = ['.X..XX...X', 'X.........', '.X.......X', '..........', '........X.', '.X...XXX..', '.....X..XX', '.....X.X..', '..........', '.....X..XX']
print(minimumMoves(grid, 9, 1, 9, 6))
