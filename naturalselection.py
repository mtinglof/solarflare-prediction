from creaturecreation import CreatureCreation
from createpopulation import CreatePopulation

import math 
import random
import time 
import torch
import copy
import numpy as np

class NaturalSelection(): 
    def __init__(self):

        # TODO allow for better preforming creatures to be selected more 
        self.mutation_chance = 0 
        self.max_num_of_genes = 5
        self.gene_names = ["TOTUSJH", "TOTBSQ", "TOTPOT", "TOTUSJZ", "ABSNJZH", "SAVNCPP", "USFLUX", "TOTFZ", 
        "MEANPOT", "EPSZ", "MEANSHR", "SHRGT45", "MEANGAM", "MEANGBT", "MEANGBZ", "MEANGBH", "MEANJZH", "TOTFY", 
        "MEANJZD", "MEANALP", "TOTFX", "EPSY", "EPSX", "R_VALUE", "XR_MAX"]

    def breedSpecies(self, dad, mom): 
        self.getMutationChance(mom.getCreature()["last_score"])
        
        mom_genome = mom.getCreature()['genome']
        dad_genome = dad.getCreature()['genome']
        creature = CreatureCreation()


        # TODO: Understand the difference between random number of genes and some 
        #       sort of parental influence on number of genes 
        num_genes = random.randint(1, self.max_num_of_genes)

        gene_list = []
        gene_list_names = []
        for gene in mom_genome: 
            gene_list.append(gene)
            gene_list_names.append(gene['name'])
        for gene in dad_genome: 
            if gene['name'] in gene_list_names: 
                if (random.randint(0, 1) == 0): 
                    gene_list[gene_list_names.index(gene['name'])] = gene
            else: 
                gene_list.append(gene)
                gene_list_names.append(gene['name'])

        additional_genes = 0 
        if(len(gene_list) < num_genes): 
            additional_genes = num_genes - len(gene_list)
            num_genes = len(gene_list)
        gene_indexes = random.sample(range(0, len(gene_list)), num_genes)
        
        while additional_genes > 0: 
            gene_name = random.choice(self.gene_names)
            while (gene_name in gene_list_names): 
                gene_name = random.choice(self.gene_names)
            gene_list_names.append(gene_name)
            min_gene_index = random.randint(0, 59)
            max_gene_index = random.randint(0, 59)
            while(min_gene_index > max_gene_index or max_gene_index < min_gene_index): 
                min_gene_index = random.randint(0, 59)
                max_gene_index = random.randint(0, 59)
            creature.addGene(gene_name, min_gene_index, max_gene_index)
            additional_genes -= 1


        # TODO create some sort of cross over between mom or dad 
        # TODO add mutation to genes 
        for gene_index in gene_indexes: 
            gene_name = gene_list[gene_index]['name']
            min_gene_index = gene_list[gene_index]['min']
            max_gene_index = gene_list[gene_index]['max']
            if (random.randint(0, 100) < self.mutation_chance): 
                chance = random.randint(0,7)
                if(chance == 0 | chance == 4 | chance == 6): 
                    increase_max = random.randint(1,60)
                    max_gene_index += increase_max
                if(chance == 1 | chance == 4 | chance == 7): 
                    increase_min = random.randint(1,60)
                    min_gene_index += increase_min
                if(chance == 2 | chance == 5 | chance == 7): 
                    decrease_max = random.randint(1,60)
                    max_gene_index -= decrease_max
                if(chance == 3 | chance == 5 | chance == 6): 
                    decrease_min = random.randint(1,60)
                    min_gene_index -= decrease_min

                if(max_gene_index > 59): 
                        max_gene_index = 59
                if(min_gene_index > 59): 
                    min_gene_index = 59
                if(min_gene_index < 0): 
                    min_gene_index = 0 
                if(max_gene_index < 0): 
                    max_gene_index = 0 
                if(min_gene_index > max_gene_index): 
                    min_gene_index = max_gene_index
                if(max_gene_index < min_gene_index):
                    max_gene_index = min_gene_index
                
            creature.addGene(gene_name, min_gene_index, max_gene_index)
        creature.createWeights()
        return(creature)

    def breedCreatures(self, dad, mom):
        self.getMutationChance(mom.getCreature()["last_score"])
        off_spring = copy.deepcopy(mom)
            
        mom_weights_one = mom.getCreature()['weights'][0]
        mom_weights_two = mom.getCreature()['weights'][1]
        dad_weights_one = dad.getCreature()['weights'][0]
        dad_weights_two = dad.getCreature()['weights'][1]

        shape_one = np.array(dad_weights_one).shape
        layer_one = np.random.rand(shape_one[0], shape_one[1])
        shape_two = np.array(dad_weights_two).shape
        layer_two = np.random.rand(shape_two[0], shape_two[1])

        dad_one_spots = np.asarray(.5 < layer_one, dtype=int)
        mom_one_spots = np.asarray(dad_one_spots == 0, dtype=int)
        dad_two_spots = np.asarray(.5 < layer_two, dtype=int)
        mom_two_spots = np.asarray(dad_two_spots == 0, dtype=int)

        dad_one_carry = np.multiply(dad_weights_one, dad_one_spots)
        mom_one_carry = np.multiply(mom_weights_one, mom_one_spots)
        dad_two_carry = np.multiply(dad_weights_two, dad_two_spots)
        mom_two_carry = np.multiply(mom_weights_two, mom_two_spots)

        offspring_layer_one = (np.add(dad_one_carry, mom_one_carry))
        offspring_layer_two = (np.add(dad_two_carry, mom_two_carry))

        layer_one, layer_two = self.mutateCreature(offspring_layer_one, offspring_layer_two)
        off_spring.setWeights(layer_one, layer_two)
        return(off_spring)

    def mutateCreature(self, offspring_layer_one, offspring_layer_two):
        shape_one = offspring_layer_one.shape
        shape_two = offspring_layer_two.shape

        mutation_chance_one = np.random.rand(shape_one[0], shape_one[1])
        mutation_chance_two = np.random.rand(shape_two[0], shape_two[1])

        mutation_array_one = torch.randn(shape_one[0], shape_one[1])
        mutation_array_two = torch.randn(shape_two[0], shape_two[1])

        offspring_spots_one = np.asarray(offspring_layer_one > self.mutation_chance, dtype=int)
        mutation_spots_one = np.asarray(offspring_spots_one == 0, dtype=int)
        offspring_spots_two = np.asarray(offspring_layer_two > self.mutation_chance, dtype=int)
        mutation_spots_two = np.asarray(offspring_spots_two == 0, dtype=int)

        offspring_carry_one = np.multiply(offspring_layer_one, offspring_spots_one)
        offspring_carry_two = np.multiply(offspring_layer_two, offspring_spots_two)
        mutation_carry_one = np.multiply(mutation_array_one, mutation_spots_one)
        mutation_carry_two = np.multiply(mutation_array_two, mutation_spots_two)

        layer_one = np.add(offspring_carry_one, mutation_carry_one)
        layer_two = np.add(offspring_carry_two, mutation_carry_two)

        layer_one = torch.as_tensor(layer_one, dtype=torch.float32)
        layer_two = torch.as_tensor(layer_two, dtype=torch.float32)
        return (layer_one, layer_two)

    def getMutationChance(self, score): 
        try: 
            self.mutation_chance =  int(math.log(1/score)*100)
        except OverflowError: 
            self.mutation_chance = 50