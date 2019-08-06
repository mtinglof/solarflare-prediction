import random 
import copy 
from creaturecreation import CreatureCreation

class CreatePopulation(): 
    def __init__(self): 
        self.max_number_of_genes = 5
        self.gene_names = ["TOTUSJH", "TOTBSQ", "TOTPOT", "TOTUSJZ", "ABSNJZH", "SAVNCPP", "USFLUX", "TOTFZ", 
        "MEANPOT", "EPSZ", "MEANSHR", "SHRGT45", "MEANGAM", "MEANGBT", "MEANGBZ", "MEANGBH", "MEANJZH", "TOTFY", 
        "MEANJZD", "MEANALP", "TOTFX", "EPSY", "EPSX", "R_VALUE", "XR_MAX"]

    def generateStartingPopulation(self, size): 
        population_pool = []
        for pop_index in range(0, size): 
            number_of_genes = random.randint(1, self.max_number_of_genes)
            gene_name_index = random.sample(self.gene_names, number_of_genes)
            creature = CreatureCreation()
            for gene in gene_name_index: 
                gene_name = gene
                min_gene_index, max_gene_index = self.getGeneLength()
                creature.addGene(gene_name, min_gene_index, max_gene_index)
            creature.createWeights()
            population_pool.append(creature)
        return(population_pool)

    def generateStartingSpecies(self, creatures, size_of_species): 
        creature_collection = []
        for creature in creatures: 
            species_specs = {
                'high_score' : 0, 
                'creatures' : []
            }
            species_specs['creatures'].append(creature)
            for index in range(0, size_of_species): 
                off_spring = copy.deepcopy(creature)
                off_spring.createWeights()
                species_specs['creatures'].append(off_spring)
            creature_collection.append(species_specs)
        return(creature_collection)

    def getGeneLength(self): 
        min_gene_index = random.randint(0, 59)
        max_gene_index = random.randint(0, 59)
        while(min_gene_index > max_gene_index or max_gene_index < min_gene_index): 
            min_gene_index = random.randint(0, 59)
            max_gene_index = random.randint(0, 59)
        return(min_gene_index, max_gene_index)