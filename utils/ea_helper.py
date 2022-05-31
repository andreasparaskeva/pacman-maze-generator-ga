import time
import numpy as np
import os, os.path
from collections import namedtuple


FunctionCall = namedtuple('FunctionCall', field_names=['func_name', 'parameters'])

def column(matrix, i):
  return [row[i] for row in matrix]

def pad_with_wall(vector, pad_width, iaxis, kwargs):
  pad_value = kwargs.get('padder', '%')
  vector[:pad_width[0]] = pad_value
  vector[-pad_width[1]:] = pad_value
  return vector

def pad_with_food(vector, pad_width, iaxis, kwargs):
  pad_value = kwargs.get('padder', '.')
  vector[:pad_width[0]] = pad_value
  vector[-pad_width[1]:] = pad_value
  return vector

def rot360(matrix, flag=False):
  return matrix

def rot90(matrix, flag=False):
  return list(zip(*matrix[::-1])) if (not flag) else np.fliplr(list(zip(*matrix[::-1])))

def rot180(matrix, flag=False):
    return rot90(rot90(matrix), flag)

def rot270(matrix, flag=False):
    return rot90(rot180(matrix), flag)


invalid_2d = [
  # 1
  [
    ['.', '.'],
    ['.', '.'],
  ],
  # 2
  [
    ['.', '%'],
    ['%', '.'],
  ], 
  # 3
  [
    ['%', '%'],
    ['%', '%'],
  ], 
]

invalid_3d = [
  # 1
  [
    ['.', '.', '.'],
    ['.', '%', '.'],
    ['.', '.', '.'],
  ],
  # 2
  [
    ['.', '.', '.'],
    ['.', '%', '%'],
    ['%', '%', '.'],
  ],
  # 3
  [
    ['%', '%', '.'],
    ['.', '%', '.'],
    ['.', '%', '%'],
  ],
  # 4
  [
    ['.', '%', '%'],
    ['%', '%', '.'],
    ['.', '%', '.'],
  ],
]

invalid_2x3 = [
  [
    ['%', '%', '%'],
    ['%', '.', '%'],
  ],
  [
    ['%', '.', '%'],
    ['%', '%', '%'],
  ]
]

invalid_3x2 = [
  [
    ['%', '%'],
    ['%', '.'],
    ['%', '%'],
  ],
  [
    ['%', '%'],
    ['.', '%'],
    ['%', '%'],
  ]
]

# valid blocks
Blocks = [
  # 1
  [
    ['%', '%', '%'],
    ['.', '.', '.'],
    ['%', '%', '%'],
  ],
  # 2
  [
    ['%', '%', '.'],
    ['%', '.', '.'],
    ['%', '.', '%'],
  ],
  # 3
  [
    ['.', '.', '.'],
    ['%', '%', '%'],
    ['.', '.', '.'],
  ],
  # 4
  [
    ['%', '%', '%'],
    ['%', '.', '.'],
    ['%', '.', '%'],
  ],
  # 5
  [
    ['.', '.', '.'],
    ['.', '%', '.'],
    ['%', '%', '%'],
  ],
  # 6
  [
    ['.', '%', '.'],
    ['%', '%', '%'],
    ['.', '%', '.'],
  ],
  # 7
  [
    ['.', '%', '.'],
    ['%', '%', '%'],
    ['.', '.', '.'],
  ],
  # 8
  [
    ['.', '%', '%'],
    ['.', '%', '.'],
    ['.', '%', '.'],
  ],
  # 9
  [
    ['.', '.', '%'],
    ['%', '.', '%'],
    ['.', '.', '%'],
  ],
]

functionList = {
  'rot90': rot90,
  'rot180': rot180,
  'rot270': rot270,
  'rot360': rot360
}

"""
Mapping from blocktypes to different variations of block
"""
block_combos = [
  FunctionCall('rot90', {'flag': False}),
  FunctionCall('rot90', {'flag': True}),
  FunctionCall('rot180', {'flag': False}),
  FunctionCall('rot180', {'flag': True}),
  FunctionCall('rot270', {'flag': False}),
  FunctionCall('rot270', {'flag': True}),
  FunctionCall('rot360', {'flag': False}),
  FunctionCall('rot360', {'flag': True}),
]

block2d = [
  ['.', '%'],
  ['.', '.']
]

def get_invalid():
  all_invalid_2d = list()
  all_invalid_3d = list()
  for invalid in invalid_2d:
    for function_call in block_combos:
      func_name = function_call.func_name
      parameters = function_call.parameters
      block = np.array(functionList[func_name](invalid, **parameters)).flatten()
      all_invalid_2d.append(tuple(block))
  for invalid in invalid_3d:
    for function_call in block_combos:
      func_name = function_call.func_name
      parameters = function_call.parameters
      block = np.array(functionList[func_name](invalid, **parameters)).flatten()
      all_invalid_3d.append(tuple(block))
  return (set(all_invalid_2d), set(all_invalid_3d))


def get_valid():
  all_valid_3d = list()
  for valid in Blocks:
    for function_call in block_combos:
      func_name = function_call.func_name
      parameters = function_call.parameters
      block = np.array(functionList[func_name](valid, **parameters)).flatten()
      all_valid_3d.append(tuple(block))
  return set(all_valid_3d)

def get_all_2d():
  all_2x2 = list()
  for function_call in block_combos:
    func_name = function_call.func_name
    parameters = function_call.parameters
    block = np.array(functionList[func_name](block2d, **parameters)).flatten()
    all_2x2.append(tuple(block))
  return set(all_2x2)
  
def get_positions(row, col, row_lenght, col_lenght, blocks_per_row):
  p1 = row//3
  p2 = (row+row_lenght)//3
  p3 = col//3
  p4 = (col+col_lenght)//3
  return set([p1*blocks_per_row+p3, p1*blocks_per_row+p4, p2*blocks_per_row+p3, p2*blocks_per_row+p4])


invalid = [
  [
    ['%', '%', '%'],
    ['%', '.', '%'],
    ['%', '.', '%'],
  ],
  [
    ['%', '.', '%'],
    ['%', '.', '%'],
    ['%', '%', '%'],
  ]
]

small_p = [
      ['%', '%', '%'],
      ['%', '.', '%'],
      ['.', '.', '.']
]
small_p_fix = [
      ['%', '%', '%'],
      ['%', '%', '%'],
      ['.', '.', '.']
]
big_p = [
      ['%', '%', '%'],
      ['%', '.', '%'],
      ['%', '.', '%']
]
big_p_fix = [
      ['%', '%', '%'],
      ['%', '%', '%'],
      ['%', '%', '%']
]

# Dead end block and fix
fix_dead_end = [
                ['%', '%'],
                ['%', '%'],
                ['%', '%']
]
dead_end = [
                ['%', '%'],
                ['%', '.'],
                ['%', '%']
]

def cornerCase(d):
  # top left corner
  if d[2, 2] == '%' and d[2,3] == '.' and d[3,2] == '.':
    d[1,2] = '%'
    d[1,1] = '%'
    d[2,1] = '%'

  # top right corner
  if d[2, d.shape[1]-3] == '%' and d[2,d.shape[1]-4] == '.' and d[3,d.shape[1]-3] == '.':
    d[1,d.shape[1]-2] = '%'
    d[1,d.shape[1]-3] = '%'
    d[2,d.shape[1]-2] = '%'

  # bottom left corner
  if d[d.shape[0]-3, 2] == '%' and d[d.shape[0]-3,3] == '.' and d[d.shape[0]-4,2] == '.':
    d[d.shape[0]-2,2] = '%'
    d[d.shape[0]-2,1] = '%'
    d[d.shape[0]-3,1] = '%'

  # bottom right corner
  if d[d.shape[0]-3, d.shape[1]-3] == '%' and d[d.shape[0]-3,d.shape[1]-4] == '.' and d[d.shape[0]-4,d.shape[1]-3] == '.':
    d[d.shape[0]-2,d.shape[1]-2] = '%'
    d[d.shape[0]-2,d.shape[1]-3] = '%'
    d[d.shape[0]-3,d.shape[1]-2] = '%'

def manhattan(a, b):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))

def maxDist(points):
    max_dist = 0
    max_dist_points = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            curr_dist = manhattan(points[i], points[j])
            if max_dist < curr_dist:
                max_dist = curr_dist
                max_dist_points = (points[i], points[j])
                idx = [i, j]

    return max_dist_points, idx

def fix_side_dead_end(d):
  # check left side
  dead_end_flat = set(tuple(np.array(dead_end).flatten()))
  for r in range(1, d.shape[0]-3):
    curr = d[r:r+3, 0:2]
    curr = tuple(np.array(curr).flatten())
    if curr in dead_end_flat:
      d[r:r+3, 0:2] = fix_dead_end

  # check right side
  dead_end_flat = set(tuple(np.fliplr(dead_end).flatten()))
  for r in range(1, d.shape[0]-3):
    curr = d[r:r+3, d.shape[1]-2:d.shape[1]]
    curr = tuple(np.array(curr).flatten())
    if curr in dead_end_flat:
      d[r:r+3, d.shape[1]-2:d.shape[1]] = fix_dead_end

  # check top side
  dead_end_flat = set(tuple(np.array(dead_end).flatten()))
  for c in range(2, d.shape[1]-4):
    curr = d[0:2, c:c+3]
    curr = tuple(np.array(curr).flatten())
    if curr in dead_end_flat:
      d[0:2, c:c+3] = fix_dead_end

  # check bottom side
  dead_end_flat = set(tuple(np.fliplr(dead_end).flatten()))
  for c in range(2, d.shape[1]-4):
    curr = d[d.shape[0]-4:d.shape[0]-1, c:c+3]
    curr = tuple(np.array(curr).flatten())
    if curr in dead_end_flat:
      d[d.shape[0]-2:d.shape[0], c:c+3] = fix_dead_end

def get_middle_point(column_size):
  return column_size//2

def fix_pi_middle(d):
  # fix Pi shape |_|
  for r in range(1, d.shape[0]-3):
    # getting the next middle block (3x3).
    middle_column_point = get_middle_point(column_size=d.shape[1])
    curr = d[r:r+3, middle_column_point-1:middle_column_point+2]
    curr = tuple(np.array(curr).flatten())
    if curr == tuple(np.array(small_p).flatten()):
      d[r:r+3, middle_column_point-1:middle_column_point+2] = small_p_fix
    if curr == tuple(np.array(big_p).flatten()):
      d[r:r+3, middle_column_point-1:middle_column_point+2] = big_p_fix
    if curr == tuple(np.flipud(small_p).flatten()):
      d[r:r+3, middle_column_point-1:middle_column_point+2] = np.flipud(small_p_fix)
    if curr == tuple(np.flipud(big_p).flatten()):
      d[r:r+3, middle_column_point-1:middle_column_point+2] = np.flipud(big_p_fix)

def add_pacman_ghosts(d):
  # add pacman and ghosts
  row, col = np.where(d == '.')
  indices_list = list(zip(row, col))
  indices = np.random.choice(len(indices_list), 6)
  indices_list = np.array(indices_list)
  max_dist_points, idx = maxDist(indices_list[indices])
  indices = np.delete(indices, idx)
  rP, cP = max_dist_points[0]
  rG, cG = max_dist_points[1]
  d[rP,cP] = 'P'
  d[rG,cG] = 'G'
  for i in range(len(indices)):
    r, c = indices_list[indices[i]]
    d[r,c] = 'o'

def finalize_maze(d):
  # add food in inner wall were necessary
  for r in range(2, d.shape[0]-2):
    if d[r, d.shape[1]-3] == '%':
      d[r-1, d.shape[1]-2] = '.'
      d[r, d.shape[1]-2] = '.'
      d[r+1, d.shape[1]-2] = '.'
      if d[r-1, d.shape[1]-3] != '%' and d[r+1, d.shape[1]-3] != '%' and d[r, d.shape[1]-4] != '%':
        d[r, d.shape[1]-2] = '%'
      
  for c in range(2, d.shape[1]-2):
    if d[2,c] == '%':
      d[1,c-1] = '.'
      d[1,c] = '.'
      d[1,c+1] = '.'
      if d[2,c-1] != '%' and d[2,c+1] != '%' and  d[3,c] != '%':
        d[2,c] = '%'
    
  for r in range(2, d.shape[0]-2):
    if d[r,2] == '%':
      d[r-1,1] = '.'
      d[r,1] = '.'
      d[r+1,1] = '.'
      if d[r-1,2] != '%' and d[r+1,2] != '%' and d[r,3] != '%':
        d[r,1] = '%'

  for c in range(2, d.shape[1]-2):
    if d[d.shape[0]-3,c] == '%':
      d[d.shape[0]-2,c-1] = '.'
      d[d.shape[0]-2,c] = '.'
      d[d.shape[0]-2,c+1] = '.'
      if d[d.shape[0]-3,c-1] != '%' and d[d.shape[0]-3,c+1] != '%' and d[d.shape[0]-4,c] != '%':
        d[d.shape[0]-3,c] = '%'

  invalid_set = set([tuple(np.array(pattern).flatten()) for pattern in invalid])
  full_block = [
                  ['%', '%', '%'],
                  ['%', '%', '%'],
                  ['%', '%', '%']
                ]
  col = d.shape[1]//2
  for row in range(0, d.shape[0]-2):
    curr = d[row:row+3, col:col+3]
    curr = tuple(np.array(curr).flatten())
    if curr in invalid_set:
      d[row:row+3, col:col+3] = full_block

  cornerCase(d)

  fix_pi_middle(d)
 
  fix_side_dead_end(d)

  add_pacman_ghosts(d)


  # saving the output file
  _, _, files = next(os.walk("./examples"))
  file_count = len(files)
  with open(f'examples/{file_count}_out_({d.shape[0]},{d.shape[1]}).lay', 'w') as f:
    for row in range(d.shape[0]):
      line = ''.join(d[row])
      f.write(f'{line}\n')