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
        self.training_set = self.training_set.drop(["XR_MAX", "MEANPOT"], axis = 1) 

    def getClassTestData(self):
        self.training_class = self.test_obj.getClassTestData()

    def testCreatures(self, creature_collection): 
        whole_start = time.time()
        creature_input = self.getTransformedCreatureData()
        input_end = time.time() - whole_start
        score_count = 0 
        for creature in creature_collection: 
            start = time.time()
            model = Neural_Network(creature.input_length, creature.hidden_length)
            model.setWeights(creature.getCreature()["weights"])
            predict = model.forward(torch.tensor(creature_input, dtype=torch.float))
            np_predict = np.asarray(predict[:,0] < predict[:,1], dtype=int)
            score = f1_score(self.training_class, np_predict)
            creature.setLastScore(score)
            score_count += 1
        end = time.time() - whole_start
        test_end = time.time() - start
        print("creature input {}".format(input_end))
        print("creature test {}".format(test_end))    
        print("whole test time {}".format(end))
        print(score_count)

    def getTransformedCreatureData(self): 
        full_data = self.training_set
        names = full_data.columns 
        aic_hold = []
        obs = len(full_data)/60
        min_row = 0 
        max_row = 60
        fit_collect = 0 
        for x in range(0, int(obs)): 
            aic_row = []
            for index, name in enumerate(names): 
                parameter = self.time_mean_sd['ARIMA'][index]
                test_data = full_data[name][min_row:max_row]
                start = time.time()
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    thing_start = time.time()
                    model = tsmodel.ARIMA(test_data, (int(parameter[1]), int(parameter[4]), int(parameter[7])))
                    aic = model.fit().aic
                    fit_collect += ((time.time()) - thing_start)
                end = time.time() - start
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
        print('fitting took {}'.format(fit_collect))
        return(np.array(aic_hold))