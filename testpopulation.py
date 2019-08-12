from gettrainingset import GetTrainingSet 
from createpopulation import CreatePopulation
from neuralnetwork import Neural_Network
from sklearn.metrics import f1_score 

import pandas as pd 
import numpy as np 
import copy
import torch
import time

# OUTDATED, DO NOT USE

class TestPopulation(): 
    def __init__(self, size, survival_threshold): 
        self.training_set_size = size 
        self.training_obj = GetTrainingSet(self.training_set_size)
        self.training_set_series = []
        self.training_class_series = []
        self.survival_threshold = survival_threshold
        self.test_round_count = -1

    def getTestData(self): 
        self.training_set_series.append(self.training_obj.getTestData())

    def getClassTestData(self):
        self.training_class_series.append(self.training_obj.getClassTestData())
        self.test_round_count += 1

    def resetTesting(self): 
        self.training_class_series = []
        self.training_set_series = []
        self.test_round_count = -1

    def setPopulation(self, population): 
        self.creature_collection_to_test = population

    def setThreshold(self, threshold): 
        self.survival_threshold = threshold

    def testPopulation(self, species): 
        tested_species = species
        for index, test_data in enumerate(self.training_set_series): 
            if len(tested_species) == 0: 
                break
            self.full_training_set = test_data
            creature_class = self.training_class_series[index]
            creature_test_data = self.getTransformedCreatureData(tested_species[0])
            creature_test_data = np.array(creature_test_data)
            creature_test_data = np.transpose(creature_test_data)
            passed_creatures = []
            for creature in tested_species: 
                model = Neural_Network(creature.getCreature()["input_length"], creature.getCreature()["hidden_length"])
                model.setWeights(creature.getCreature()["weights"])
                predict = model.forward(torch.tensor(creature_test_data, dtype=torch.float))
                np_predict = np.asarray(predict[:,0] < predict[:,1], dtype=int)
                score = f1_score(creature_class, np_predict)
                if score > self.survival_threshold: 
                    creature.getCreature()['last_score'] = score
                    try: 
                        creature.setScore(index, score)
                    except TypeError: 
                        creature.addScore(score)
                    except IndexError: 
                        creature.addScore(score) 
                    passed_creatures.append(creature)
            tested_species = passed_creatures
        return(tested_species)

    def getTransformedCreatureData(self, creature): 
        col_names = True
        column_names = []
        transformed_data = []
        creature_genome = creature.getCreature()["genome"]
        for gene in creature_genome: 
            gene_min_index = gene['min']
            gene_max_index = gene['max']
            gene_name = gene['name']
            for index in range(gene_min_index, gene_max_index+1): 
                gene_data = pd.DataFrame(self.full_training_set[gene_name][index]).transpose()
                if(col_names): 
                    for col_index in range(0, gene_data.shape[1]): 
                        column_names.append(col_index)
                    col_names = False
                gene_data.columns = column_names
                transformed_data.append(gene_data)
        return(pd.concat(transformed_data)) 