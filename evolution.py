import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import sys

### GLOBAL VARIABLES ###


### GENETIC ALGORITHM CLASS ###
# Description: Includes the methods of the GA to initialize, select, breed, and mutate chromosomes
class Offspring():
    # Initializes chromosome
    def __init__(self, id, first_gen = True, mutant = False, child = False, parent1 = None, parent2 = None):
        ### CHROMOSOME ###
        # Genes: [
        # Generator Learning Rate -     0.0-1.0
        # Discriminator Learning Rate - 0.0-1.0
        # Epochs -                      32-256
        # Steps -                       32-512
        # Activation Function -         1=RELU, 2=SIGMOID
        # Generator Dropout Rate -      0.0-1.0
        # Discriminator Dropout Rate -  0.2-0.5
        # ]
        self.chromosome = []
        self.chromosome_types = [float, float, int, int, int, float, float]
        self.gene_map = [[0.0001, 0.01], [0.0001, 0.01], [32, 128], [32, 512], [0, 4], [0.2, 0.5], [0.2, 0.5]] # Must be the same length as chromosome, but each item must be a list of possible values

        for i in range(len(self.chromosome_types)):
            self.chromosome.append(self.gene_map[i][0])

        self.breed_avg = True # If true the child chromosome will be an average of the two parents, if false the child chromosome will be a rand value between the two
        self.mutation_odds = 0.2
        self.mutation_rate = 0.001

        self.alive = True
        self.id = id
        self.fitness = 0
        self.age = 0

        self.mutant = mutant # One parent (self)
        self.child = child # Two parents
        self.parent1 = parent1
        self.parent2 = parent2

        if(len(self.chromosome) is not len(self.gene_map)):
            print("Error: Chromosome and Gene Map are not the same size.\nChromosome Length:", len(self.chromosome), "\nGene Map Length:", len(self.gene_map))
            sys.exit()
        
        # Generate weights
        if(first_gen):
            self.generate_chromosome()
        elif(mutant):
            self.mutate()
        elif(child):
            self.breed()

    def generate_chromosome(self):

        for i, g in enumerate(self.chromosome_types):
            if(type(g) is bool):
                self.chromosome[i] = random.choice(True, False)
            elif(type(g) is int):
                self.chromosome[i] = random.randint(self.gene_map[i][0], self.gene_map[i][1])
            elif(type(g) is float):
                self.chromosome[i] = random.randrange(self.gene_map[i][0], self.gene_map[i][1])


    def mutate(self):

        for g, i in enumerate(self.chromosome):

            mutator = random.random()
            direction = random.choice(1, -1)

            if(type(g) is int and mutator < self.mutation_odds):
                self.chromosome[i] += direction
            elif(type(g) is float and mutator < self.mutation_odds):
                mr = self.mutation_rate * random.randint(0, 25)
                self.chromosome[i] = mr * direction

    def breed(self):

        self.fitness = (self.parent1.fitness + self.parent2.fitness) / 2

        for g, i in enumerate(self.chromosome):
            if(type(g) is bool):
                if(self.parent1.chromosome[i] is self.parent2.chromosome[i]):
                    self.chromosome[i] = self.parent1.chromosome[i]
                else:
                    self.chromosome[i] = random.choice(True, False)

            if(self.breed_avg):
                if(type(g) is int):
                    self.chromosome[i] = np.floor((self.parent1.chromosome[i] + self.parent2.chromosome[i]) / 2)

                elif(type(g) is float):
                    self.chromosome[i] = (self.parent1.chromosome[i] + self.parent2.chromosome[i]) / 2
            else:
                if(type(g) is int):
                    self.chromosome[i] = random.randint(self.parent1.chromosome[i], self.parent2.chromosome[i])

                elif(type(g) is float):
                    self.chromosome[i] = random.randrange(self.parent1.chromosome[i], self.parent2.chromosome[i])

    def step(self):
        self.fitness += 0.1
        self.age += 1

    def die(self):

        print("-----GAN", self.id, "HAS DIED-----")
        print(self.chromosome)
        print("---FITNESS---")
        print(self.fitness)
        print("---Age---")
        print(self.age)