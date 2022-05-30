import numpy as np
from model import Population, Individual
from maze import MazeGenerator

def create_population(pop_size, shape) -> Population:
  individuals = []
  for i in range(pop_size):
    new = MazeGenerator(shape[0], shape[1])
    block_fitness = np.zeros((shape[0]//3)*(shape[1]//3))
    individuals.append(Individual(genotype=new, block_fitness=block_fitness))

  return Population(individuals=individuals)


