from model import Population, Pair, Individual
from typing import List
import numpy as np

class Selection:
  def select_pairs(self, population: Population) -> List[Pair]:
    pass

class TournamentSelection(Selection):
  def __init__(self, k, factor=1.0):
    self.k = k
    self.factor = factor

  def info(self):
    return f'tourn-{self.k}-f:{self.factor}'

  def select_pairs(self, population: Population) -> List[Pair]:
    pairs = []
    for i in range(0, int(self.factor * population.size()), 2):
      parent1 = self.select_from_tournament(population)
      parent2 = self.select_from_tournament(population)
      pairs.append(
        Pair(parent1=parent1, parent2=parent2)
      )

    return pairs

  def select_from_tournament(self, population) -> Individual:
    selected_indexes = np.random.choice(range(population.size()), size=self.k)
    best_fitness = -1
    tournament_winner = None
    for index in selected_indexes:
      if population.individuals[index].fitness > best_fitness:
        best_fitness = population.individuals[index].fitness
        tournament_winner = population.individuals[index]

    return tournament_winner

class ProportionalSelection(Selection):

  def __init__(self, factor=1.0):
    self.factor = factor

  def info(self):
    return f'roulette-f:{self.factor}'

  def select_pairs(self, population: Population) -> List[Pair]:
    proportioned_fitnesses = self.get_proportions_of(population.get_fitnesses())
    pairs = []
    for i in range(0, int(self.factor * population.size()), 2):
      index_o1 = np.random.choice(range(population.size()), p=proportioned_fitnesses)
      index_o2 = np.random.choice(range(population.size()), p=proportioned_fitnesses)
      pairs.append(Pair(population.individuals[index_o1], population.individuals[index_o2]))

    return pairs

  def get_proportions_of(self, fitnesses):
    f_sum = np.sum(fitnesses)
    f_min = np.min(fitnesses)

    proportioned_fitnesses = fitnesses.copy()
    if np.all(fitnesses == fitnesses[0]) or f_sum - f_min * len(fitnesses) == 0.0:
      return [1 / len(fitnesses) for i in range(len(fitnesses))]

    for index, val in enumerate(fitnesses):
      proportioned_fitnesses[index] = (proportioned_fitnesses[index] - f_min) / (f_sum - f_min * len(fitnesses))

    return list(proportioned_fitnesses)
