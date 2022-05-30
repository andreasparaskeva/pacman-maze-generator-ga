import numpy as np
from numpy.random import rand
from model import Pair, Individual
from typing import List

class Crossover():
  def apply(self, parents: Pair, fitnesses):
    pass


class UniformCrossover(Crossover):
  def __init__(self, pc, is_dynamic=False):
    self.pc = pc
    self.is_dynamic = is_dynamic

  def info(self):
    return f'unif-dynamic' if self.is_dynamic else f'unif-{self.pc}'

  def apply(self, parents: Pair, fitnesses):
    if self.is_dynamic:
      if max(fitnesses) - min(fitnesses) == 0:
        self.pc = 0
      else:
        self.pc = abs(parents.parent1.fitness - parents.parent2.fitness) / (max(fitnesses) - min(fitnesses))
    p1 = parents.parent1.copy_genotype()
    p2 = parents.parent2.copy_genotype()
    c1 = p1.copy_genotype()
    c2 = p2.copy_genotype()
    rows = p1.genotype.grid.shape[0]
    cols = p1.genotype.grid.shape[1]
    if rand() < self.pc:
      for r in range(0, rows-2, 3):
        for c in range(0, cols-2, 3):
          if rand() < 0.5:
            c1.genotype.grid[r:r+3, c:c+3] = p2.genotype.grid[r:r+3, c:c+3]
            c2.genotype.grid[r:r+3, c:c+3] = p1.genotype.grid[r:r+3, c:c+3]
    return [c1, c2]
