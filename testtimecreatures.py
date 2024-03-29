from gettrainingset import GetTrainingSet
from neuralnetwork import Neural_Network
#import statsmodels.tsa.arima_model as tsmodel 
from sklearn.metrics import f1_score 

import rpy2
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

import numpy as np 
import pandas as pd 
import torch 
import warnings
import time

class TestTimeCreatures: 
    def __init__(self): 
        self.time_mean_sd = pd.read_csv('time_series_mean_sd.csv')
        self.test_obj = GetTrainingSet()

        base = importr('base')
        utils = importr('utils')
        utils.chooseCRANmirror(ind=1) 
        utils.install_packages('forecast')
        self.arima = robjects.r['arima']

    def getTestData(self, size): 
        #print("getting training set...")
        self.training_set = self.test_obj.getTestData(size)
        #print("done")
        #self.training_set = self.training_set.drop(["XR_MAX", "MEANPOT"], axis = 1) 

    def getClassTestData(self):
        self.training_class = self.test_obj.getClassTestData()

    def testCreatures(self, creature_collection): 
        #print("fitting...")
        creature_input = self.getTransformedCreatureData()
        #print("done")
        #print("testing...")
        #whole_time = 0 
        for creature in creature_collection: 
            #start = time.time()
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
            #whole_time += time.time() - start
        #print(whole_time)
        #print("done")

    def getTransformedCreatureData(self): 
        full_data = self.training_set
        names = full_data.columns 
        aic_hold = []
        obs = len(full_data)/60
        min_row = 0 
        max_row = 60
        #whole_time = 0 
        for x in range(0, int(obs)): 
            aic_row = []
            for index, name in enumerate(names): 
                parameter = self.time_mean_sd['ARIMA'][index]
                test_data = full_data[name][min_row:max_row]
                # with warnings.catch_warnings():
                #     warnings.simplefilter("ignore")
                    # model = tsmodel.ARIMA(test_data, (int(parameter[1]), int(parameter[4]), int(parameter[7])))
                    # aic = model.fit(disp=False).aic
                #start = time.time()
                aic = self.arima(robjects.FloatVector(test_data), robjects.IntVector([int(parameter[1]), int(parameter[4]), int(parameter[7])]))[5][0] 
                #whole_time += time.time() - start
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
        #print(whole_time)
        return(np.array(aic_hold))