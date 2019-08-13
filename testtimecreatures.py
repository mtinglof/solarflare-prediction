from gettrainingset import GetTrainingSet
from neuralnetwork import Neural_Network
import statsmodels.tsa.arima_model as tsmodel 
from sklearn.metrics import f1_score 

import numpy as np 
import pandas as pd 
import torch 
import warnings
import time

class TestTimeCreatures: 
    def __init__(self): 
        self.time_mean_sd = pd.read_csv('time_series_mean_sd.csv')
        self.test_obj = GetTrainingSet()

    def getTestData(self, size): 
        self.training_set = self.test_obj.getTestData(size)
        #self.training_set = self.training_set.drop(["XR_MAX", "MEANPOT"], axis = 1) 

    def getClassTestData(self):
        self.training_class = self.test_obj.getClassTestData()

    def testCreatures(self, creature_collection): 
        creature_input = self.getTransformedCreatureData()
        for creature in creature_collection: 
            model = Neural_Network(creature.input_length, creature.hidden_length)
            model.setWeights(creature.getCreature()["weights"])
            predict = model.forward(torch.tensor(creature_input, dtype=torch.float))
            np_predict = np.asarray(predict[:,0] < predict[:,1], dtype=int)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                score = f1_score(self.training_class, np_predict)
            if score > creature.getCreature()['best_score']: 
                creature.getCreature()['best_score'] = score
                creature.getCreature()['best_position'] = creature.getCreature()['weights']
            creature.getCreature()['last_score'] = score
            creature.getCreature()['scores'].append(score)

    def getTransformedCreatureData(self): 
        full_data = self.training_set
        names = full_data.columns 
        aic_hold = []
        obs = len(full_data)/60
        min_row = 0 
        max_row = 60
        for x in range(0, int(obs)): 
            aic_row = []
            for index, name in enumerate(names): 
                parameter = self.time_mean_sd['ARIMA'][index]
                test_data = full_data[name][min_row:max_row]
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    model = tsmodel.ARIMA(test_data, (int(parameter[1]), int(parameter[4]), int(parameter[7])))
                    aic = model.fit(disp=False).aic
                none_aic_sd = (aic - self.time_mean_sd['Mean 0'][index])/self.time_mean_sd['SD 0'][index]
                solar_aic_sd = (aic - self.time_mean_sd['Mean 1'][index])/self.time_mean_sd['SD 1'][index]
                if(name == 'R_VALUE'): 
                    if(np.isnan(none_aic_sd) or np.isnan(solar_aic_sd)): 
                        none_aic_sd = 0 
                        solar_aic_sd = 0 
                        aic_row.append(1)
                    else:
                        aic_row.append(0)
                aic_row.append(none_aic_sd)
                aic_row.append(solar_aic_sd)
            aic_hold.append(aic_row)
            min_row = min_row + 60
            max_row = max_row + 60
        return(np.array(aic_hold))