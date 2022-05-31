from tkinter import filedialog
import numpy as np
from dataclasses import dataclass
from enum import Enum
import random
from collections import namedtuple
from utils.ea_helper import pad_with_food, pad_with_wall, Blocks, functionList, block_combos

'''
  wall: '%',
  food: '.',
  energizer: 'o',
  empty: ' ',
  pacman: 'P',
  ghost: 'G',
'''


L_shape = [
            [0, 1],
            [0, 1],
            [1, 1]
    ],


class MazeGenerator:

  def __init__(self, rows, cols, root=None):
    """
    Initialize MazeGenerator object and generate empty grid
    """
    self.r = rows
    self.c = cols
    self.grid = np.empty((rows, cols,), dtype=str)
    for r in range(0, rows-2, 3):
      for c in range(0, cols-2, 3):
        # A[r:r+B.shape[0], c:c+B.shape[1]] += B
        block = self.select_random_block()
        self.grid[r:r+block.shape[0], c:c+block.shape[1]] = block
  
  def copy(self):
    maze = MazeGenerator(self.r, self.c)
    maze.grid = self.grid
    return maze

  def mirror(self):
    # add a flipped symmetric copy to the right side
    flipped = np.fliplr(np.array(self.grid))
    # delete one column after mirroring and concatenate
    self.grid = np.concatenate((np.delete(self.grid, -1, axis=1), flipped), axis=1)
    # add walls to sides (padding)
    self.grid = np.pad(self.grid, ((1, 1),(1,1)), pad_with_wall)
    self.grid = np.pad(self.grid, ((1, 1),(1,1)), pad_with_wall)

    # fix inner pad with food
    for c in range(2, self.grid.shape[1]-2):
      if self.grid[2,c] == '%':
        self.grid[1,c-1] = '.'
        self.grid[1,c] = '.'
        self.grid[1,c+1] = '.'
        
    for r in range(2, self.grid.shape[0]-2):
      if self.grid[r,2] == '%':
        self.grid[r-1,1] = '.'
        self.grid[r,1] = '.'
        self.grid[r+1,1] = '.'

    for r in range(2, self.grid.shape[0]-2):
      if self.grid[r, self.grid.shape[1]-3] == '%':
        self.grid[r-1, self.grid.shape[1]-2] = '.'
        self.grid[r, self.grid.shape[1]-2] = '.'
        self.grid[r+1, self.grid.shape[1]-2] = '.'

    for c in range(2, self.grid.shape[1]-2):
      if self.grid[self.grid.shape[0]-3,c] == '%':
        self.grid[self.grid.shape[0]-2,c-1] = '.'
        self.grid[self.grid.shape[0]-2,c] = '.'
        self.grid[self.grid.shape[0]-2,c+1] = '.'

  def select_random_block(self):
    random_idx = np.random.choice(len(Blocks))
    random_idx_func = np.random.choice(len(block_combos))
    function_call = block_combos[random_idx_func]
    func_name = function_call.func_name
    parameters = function_call.parameters
    return np.array(functionList[func_name](Blocks[random_idx], **parameters))
    
  def printMaze(self):
    '''
    String wise printing of generated array
    '''
    print('\n'.join([''.join(['{:6}'.format(item) for item in row]) 
      for row in self.grid]))

    

