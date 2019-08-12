import torch

# OUTDATED, DO NOT USE

class CreatureCreation(): 
    def __init__(self): 
        self.creature_info = {
            "last_score" : 0,
            "scores" : [],
            "genome" : [], 
            "input_length" : 0,
            "hidden_length" : 0,
            "weights" : [0, 0]
        }
        self.output_size = 2

    def addGene(self, name, min_index, max_index):
        new_gene = {}
        new_gene = {
            "name" : name, 
            "min" : min_index, 
            "max" : max_index
        }
        self.creature_info["genome"].append(new_gene)

    def createWeights(self): 
        input_length = 0 
        for gene in self.creature_info["genome"]: 
            gene_length = (gene["max"] - gene["min"]) + 1
            input_length += gene_length
        self.creature_info["input_length"] = input_length
        self.creature_info["hidden_length"] = int(round(input_length+2)/2)
        current_weights = self.creature_info["weights"]
        current_weights[0] = torch.randn(self.creature_info["input_length"], self.creature_info["hidden_length"])
        current_weights[1] = torch.randn(self.creature_info["hidden_length"], self.output_size)
        self.creature_info["weights"] = current_weights

    def setWeights(self, W1, W2): 
        current_weights = self.creature_info["weights"]
        current_weights[0] = W1
        current_weights[1] = W2
        self.creature_info["weights"] = current_weights

    def setLastScore(self, score): 
        self.creature_info["last_score"] = score

    def addScore(self, score): 
        self.creature_info['scores'].append(score)

    def setScore(self, index, score): 
        self.creature_info['scores'][index] = score

    def flushScores(self): 
        self.creature_info['scores'] = []

    def getCreature(self): 
        return(self.creature_info)