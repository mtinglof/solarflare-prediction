from createpopulation import CreatePopulation
from testpopulation import TestPopulation
from operator import itemgetter
from naturalselection import NaturalSelection

import time 
import random
import copy

# OUTDATED, DO NOT USE

class MainRunner(): 
    def __init__(self, num_of_starting_species, size_of_starting_species, training_size):
        self.size_of_starting_species = size_of_starting_species-1
        self.size_of_training = training_size 
        self.num_of_starting_species = num_of_starting_species
        self.high_survival_threshold = .1
        self.survival_threshold_range = .1
        self.min_survival_threshold = self.high_survival_threshold - self.survival_threshold_range
        self.population_load_limit = 10000

    def createStartingCollection(self): 
        population_obj = CreatePopulation()
        starting_creature_collection = population_obj.generateStartingPopulation(self.num_of_starting_species)
        starting_creature_collection = population_obj.generateStartingSpecies(starting_creature_collection, self.size_of_starting_species)
        return(starting_creature_collection)

    def getTestObj(self): 
        self.test_obj = TestPopulation(self.size_of_training, self.min_survival_threshold)

    def resetTestObj(self): 
        self.test_obj.resetTesting()
        self.high_survival_threshold = .1
        self.survival_threshold_range = .1
        self.min_survival_threshold = self.high_survival_threshold - self.survival_threshold_range

    def newTestRound(self): 
        self.test_obj.getTestData()
        self.test_obj.getClassTestData()

    def testCreatures(self, creature_collection): 
        tested_creatures = []
        self.test_obj.setThreshold(self.min_survival_threshold)
        for species in creature_collection: 
            creatures = (self.test_obj.testPopulation(species['creatures']))
            if len(creatures) > 0: 
                creatures_dict = {
                    'high_score' : 0, 
                    'creatures' : creatures
                }
                tested_creatures.append(creatures_dict)
        return(tested_creatures)
        
    def sortHerd(self, creature_collection): 
        for index, species in enumerate(creature_collection): 
            creature_collection[index]['creatures'] = (sorted(species['creatures'], key = lambda creaturecreation: creaturecreation.getCreature()["last_score"], reverse=True))
            creature_collection[index]['high_score'] = creature_collection[index]['creatures'][0].getCreature()['last_score']
        return(sorted(creature_collection, key = lambda i: i["high_score"], reverse=True))

    def checkSurvival(self, creature_collection): 
        try:
            if creature_collection[0]['high_score'] > self.min_survival_threshold: 
                if creature_collection[0]['high_score'] > self.high_survival_threshold: 
                    self.high_survival_threshold = creature_collection[0]['high_score']
                    self.min_survival_threshold = creature_collection[0]['high_score'] - self.survival_threshold_range
                return True
            else: 
                return False
        except IndexError:
            return False

    def creatureNaturalSelection(self, creature_collection): 
        alphas = []
        selection_obj = NaturalSelection()
        pop_obj = CreatePopulation()

        for species in creature_collection: 
            creatures = species['creatures']
            creatures_size = len(creatures)
            new_creatures = []
            if creatures_size > 1: 
                while creatures_size < self.num_of_starting_species: 
                    mom, dad = random.sample(creatures, 2)
                    offspring = selection_obj.breedCreatures(dad, mom)
                    offspring.flushScores()
                    offspring.setLastScore(0) 
                    new_creatures.append(offspring)
                    creatures_size += 1
                species['creatures'] = species['creatures'] + new_creatures
            else: 
                selection_obj.getMutationChance(species['creatures'][0].getCreature()['last_score'])
                while creatures_size < self.num_of_starting_species: 
                    offspring = copy.deepcopy(species['creatures'][0])
                    W1, W2 = (selection_obj.mutateCreature(offspring.getCreature()['weights'][0], offspring.getCreature()['weights'][1]))
                    offspring.setWeights(W1, W2)
                    offspring.flushScores()
                    offspring.setLastScore(0)
                    species['creatures'].append(offspring)
                    creatures_size += 1
            alphas.append(species)
        return(alphas)

    def speciesNaturalSelection(self, creature_collection): 
        alpha_species = []
        selection_obj = NaturalSelection()
        pop_obj = CreatePopulation()

        for species in creature_collection: 
            creature_holder = []
            for creature in species['creatures']: 
                creature_holder.append(creature)
            alpha_species.append(creature_holder)

        alphas = self.creatureNaturalSelection(creature_collection)

        alpha_species_size = len(alpha_species)
        if alpha_species_size > 1: 
            new_species = []
            while(alpha_species_size < self.num_of_starting_species): 
                mom_species, dad_species = random.sample(alpha_species, 2)
                mom = random.sample(mom_species, 1)
                dad = random.sample(dad_species, 1)
                offspring = selection_obj.breedSpecies(dad[0], mom[0])
                new_species.append(offspring)
                alpha_species_size += 1
            return(alphas + pop_obj.generateStartingSpecies(new_species, self.size_of_starting_species))
        else: 
            additional_species = pop_obj.generateStartingPopulation(self.num_of_starting_species-1)
            return(alphas + pop_obj.generateStartingSpecies(additional_species, self.size_of_starting_species))