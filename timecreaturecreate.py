import pandas as pd 
import torch

class TimeCreatureCreate: 
    def __init__(self):
        self.mean_sd_df = pd.read_csv('time_series_mean_sd.csv')
        self.input_length = 51
        self.hidden_length = 25
        self.output_size = 2
        self.creature_info = {
            "last_score" : 0,
            "scores" : [],
            "weights" : [0, 0]
        }

    def createWeights(self): 
        current_weights = self.creature_info["weights"]
        current_weights[0] = torch.randn(self.input_length, self.hidden_length)
        current_weights[1] = torch.randn(self.hidden_length, self.output_size)
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