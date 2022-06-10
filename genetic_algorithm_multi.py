import sys
import time
import numpy as np
import model
from numpy.random import rand
from typing import List
from model import Population, Individual
from mutation import Mutation
from crossover import UniformCrossover, Crossover
from selection import ProportionalSelection, TournamentSelection, Selection
from common import create_population
from multiprocessing import Pool
from utils.ea_helper import finalize_maze


MAZE_GEN_CONFIGURATION = [
  (UniformCrossover(pc=0.7), Mutation(pm=0.5, is_dynamic=False), ProportionalSelection(factor=1.0), 4),
]

def offsprings_from(pairs, crossover, mutation: Mutation, fitnesses) -> List[Individual]:
  offsprings = list()
  for pair in pairs:
    o1, o2 = crossover.apply(pair, fitnesses)
    fitness, block_fitness = model.evaluate_fitness(o1.genotype)
    o1.fitness = fitness
    o1.block_fitness = block_fitness
    fitness, block_fitness = model.evaluate_fitness(o2.genotype)
    o2.fitness = fitness
    o2.block_fitness = block_fitness
    o1 = mutation.apply(o1)
    o2 = mutation.apply(o2)
    offsprings.append(o1)
    offsprings.append(o2)

  return offsprings

def next_population_from(offsprings: Population, population: Population) -> Population:
  parents_and_offsprings = Population(
    individuals=population.individuals.copy() + 
    offsprings.individuals.copy()
  )
  sorted_individuals = sorted(
    parents_and_offsprings.individuals,
    key=lambda x: x.fitness,
    reverse=False
  )

  return Population(individuals=sorted_individuals[:population.size()])

def genetic_search(
  selection: Selection,
  crossover: Crossover,
  mutation: Mutation,
  shape=(6,3,),
  pop_size=10,
):
  score = list()

  for r in range(1):
    f_opt = sys.maxsize
    x_opt = None

    population = create_population(pop_size, shape)
    population.evaluate_fitnesses()
    gen = 0
    while True:
      gen += 1
      if gen % 1000 == 0:
        print(f'Generation {gen}')
        for individual in population.individuals:
          print(individual.block_fitness)
      pairs = selection.select_pairs(population)
      offsprings = offsprings_from(pairs, crossover, mutation, population.get_fitnesses())
      offsprings_population = Population(individuals=offsprings)
      offsprings_population.evaluate_fitnesses()
      population = next_population_from(offsprings_population, population)
      best_individual = population.best_individual()

      if f_opt > best_individual.fitness:
        print(best_individual.fitness)
        f_opt = best_individual.fitness
        x_opt = best_individual.genotype
      if f_opt == 0:
        print(gen)
        best_individual.genotype.mirror()
        best_individual.genotype.printMaze()
        algorithm_name=f'ga_pop-{pop_size}_{selection.info()}_{crossover.info()}_{mutation.info()}'
        # np.save(f'{algorithm_name}{time.time()}.npy', best_individual.genotype.grid) 
        # finalize and save maze
        finalize_maze(best_individual.genotype.grid)
        break

  return f_opt, x_opt, score

def execute_experiment(configuration):
  (crossover, mutation, selection, population_size) = configuration
  best_fitness, _, problem_score = genetic_search(
    selection=selection,
    crossover=crossover,
    mutation=mutation,
    pop_size=population_size,
    shape=(9,9),
  )

if __name__ == '__main__':

  with Pool(8) as p:
    p.map(execute_experiment, MAZE_GEN_CONFIGURATION*2)



