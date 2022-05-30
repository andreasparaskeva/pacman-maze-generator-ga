from numpy.random import rand, binomial, sample
from model import Individual
import numpy as np
import utils.ea_helper as helper


class Mutation():
  def __init__(self, pm, is_dynamic=False):
    self.pm = pm
    self.is_dynamic = is_dynamic

  def info(self):
    return f'mut-dynamic' if self.is_dynamic else f'mut-{self.pm}'

  def apply(self, individual):
    s_pm = 0.05
    mutated = individual.copy_genotype()
    rows = mutated.genotype.grid.shape[0]
    cols = mutated.genotype.grid.shape[1]
    pos = 0
    if individual.fitness == 0:
      return mutated
    for r in range(0, rows-2, 3):
      for c in range(0, cols-2, 3):     
        # check if a mutation will take place
        # print((self.pm * (individual.block_fitness[pos]/individual.fitness)))
        if rand() < (self.pm * ((individual.block_fitness[pos]+s_pm)/individual.fitness)):
          # change the block to randonly one other choice
          unique_valid_3d = helper.get_valid()
          unique_valid_3d_list = [np.array(unique).reshape(3,3) for unique in list(unique_valid_3d)]
          random_idx = np.random.choice(len(unique_valid_3d_list))
          mutated.genotype.grid[r:r+3, c:c+3] = unique_valid_3d_list[random_idx]

        pos += 1
    return mutated

