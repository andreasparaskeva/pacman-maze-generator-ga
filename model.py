from dataclasses import dataclass
from typing import List
import numpy as np
from maze import MazeGenerator
import utils.ea_helper as helper
from utils.ea_helper import column, get_positions
from utils.ea_helper import invalid_2x3, invalid_3x2

@dataclass
class Individual:
  genotype: MazeGenerator
  block_fitness: np.ndarray
  fitness: float = None

  def size(self):
    return self.genotype.grid.shape

  def copy_genotype(self):
    return Individual(self.genotype.copy(), block_fitness=np.zeros_like(self.block_fitness))

@dataclass
class Population:
  individuals: List[Individual]

  def get_fitnesses(self):
    return np.array(list(
      map(lambda i: i.fitness, self.individuals)
    ), dtype=float)

  def get_block_fitnesses(self):
    return np.array(list(
      map(lambda i: i.block_fitness, self.individuals)
    ), dtype=float)

  def ave_fitness(self):
    return sum(individual.fitness for individual in self.individuals) / len(self.individuals)

  def average_individual(self):
    ave_fitness = self.ave_fitness()
    for i in self.individuals:
      if i.fitness == ave_fitness:
        return i

  def max_fitness(self):
    return max(individual.fitness for individual in self.individuals)

  def best_individual(self):
    min_fitness = self.min_fitness()
    for i in self.individuals:
      if i.fitness == min_fitness:
        return i

  def min_fitness(self):
    return min(individual.fitness for individual in self.individuals)

  def evaluate_fitnesses(self):
    for individual in self.individuals:
      fitness, block_fitness = evaluate_fitness(individual.genotype)
      individual.fitness = fitness
      individual.block_fitness = block_fitness
  def size(self):
    return len(self.individuals)

@dataclass
class Pair:
  parent1: Individual
  parent2: Individual

def evaluate_fitness(x:MazeGenerator):
  fitness = 0
  block_fit = np.zeros((x.grid.shape[0]//3)*(x.grid.shape[1]//3))
  unique_invalid_2d, unique_invalid_3d = helper.get_invalid()
  unique_invalid_2d_list = [np.array(unique).reshape(2,2) for unique in list(unique_invalid_2d)]
  unique_invalid_3d_list = [np.array(unique).reshape(3,3) for unique in list(unique_invalid_3d)]

  # check 2x3 violations
  for row in range(0, x.grid.shape[0]-1):
    for col in range(0, x.grid.shape[1]-2):
      curr = x.grid[row:row+2, col:col+3]
      if any([np.array_equal(curr, np.array(x)) for x in invalid_2x3]):
        positions = get_positions(row=row, col=col, row_lenght=1, col_lenght=2, blocks_per_row=x.grid.shape[1]//3)
        for pos in positions:
          block_fit[pos] += 1/len(positions)
        fitness += 1

  # check 3x2 violations
  for row in range(0, x.grid.shape[0]-2):
    for col in range(0, x.grid.shape[1]-1):
      curr = x.grid[row:row+3, col:col+2]
      if any([np.array_equal(curr, np.array(x)) for x in invalid_3x2]):
        positions = get_positions(row=row, col=col, row_lenght=2, col_lenght=1, blocks_per_row=x.grid.shape[1]//3)
        for pos in positions:
          block_fit[pos] += 1/len(positions)
        fitness += 1

  # check 3x3 violations
  for row in range(0, x.grid.shape[0]-2):
    for col in range(0, x.grid.shape[1]-2):
      curr = x.grid[row:row+3, col:col+3]
      if any([np.array_equal(curr, np.array(x)) for x in unique_invalid_3d_list]):
        positions = get_positions(row=row, col=col, row_lenght=2, col_lenght=2, blocks_per_row=x.grid.shape[1]//3)
        for pos in positions:
          block_fit[pos] += 1/len(positions)
        fitness += 1
  # check 2x2 violations
  for row in range(0, x.grid.shape[0]-1):
    for col in range(0, x.grid.shape[1]-1):
      curr = x.grid[row:row+2, col:col+2]
      if any([np.array_equal(curr, np.array(x)) for x in unique_invalid_2d_list]):
        positions = get_positions(row=row, col=col, row_lenght=1, col_lenght=1, blocks_per_row=x.grid.shape[1]//3)
        for pos in positions:
          block_fit[pos] += 1/len(positions)
        fitness += 1
  # check 4x1
  violation = list(['%', '%', '%', '%'])
  for row in range(x.grid.shape[0]):
    curr_row = x.grid[row]
    for r in (range(0, len(curr_row)-3)):
      if violation == list(curr_row[r:r+4]):
        positions = get_positions(row=row, col=r, row_lenght=0, col_lenght=3, blocks_per_row=x.grid.shape[1]//3)
        for pos in positions:
          block_fit[pos] += 1/len(positions)
        fitness += 1
  for col in range(x.grid.shape[1]):
    curr_col = column(x.grid, col)
    for c in (range(0, len(curr_col)-3)):
      if violation == list(curr_col[c:c+4]):
        positions = get_positions(row=c, col=col, row_lenght=3, col_lenght=0, blocks_per_row=x.grid.shape[1]//3)
        for pos in positions:
          block_fit[pos] += 1/len(positions)
        fitness += 1

  return fitness, block_fit
