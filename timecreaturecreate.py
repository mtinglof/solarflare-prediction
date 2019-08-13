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
            "best_score" : 0,
            "scores" : [],
            "velocity" : [0, 0], 
            "best_position" : [0, 0],
            "weights" : [0, 0]
        }

    def createWeights(self): 
        current_weights = self.creature_info["weights"]
        current_weights[0] = torch.randn(self.input_length, self.hidden_length)
        current_weights[1] = torch.randn(self.hidden_length, self.output_size)
        self.creature_info["weights"] = current_weights

    def getCreature(self): 
        return(self.creature_info)