from json import JSONDecoder, JSONDecodeError
from neuralnetwork import Neural_Network

import statsmodels.tsa.arima_model as tsmodel 
import pandas as pd
import numpy as np

import rpy2
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.rinterface import RRuntimeError

import warnings
import os
import re
import json
import torch

class SubmitCreature(): 
    def __init__(self): 
        self.path_to_data = "D:/Dev/projects/solarflare/bigdata2019-flare-prediction"
        self.file_name = "testSet.json"
        self.fname = os.path.join(self.path_to_data, self.file_name)
        self.full_data_set = []
        self.test_set = []

        self.time_mean_sd = pd.read_csv('time_series_mean_sd.csv')
        base = importr('base')
        utils = importr('utils')
        utils.chooseCRANmirror(ind=1) 
        utils.install_packages('forecast')
        self.arima = robjects.r['arima']

        self.getData()

    def getTestData(self): 
        test_frames_to_be_added = []
        for data in self.full_data_set: 
            data.set_index(data.index.astype(int), inplace = True)
            last_n_indices = np.arange(0, 60)
            data = data.loc[last_n_indices]
            test_frames_to_be_added.append(data)
        self.test_set = pd.concat(test_frames_to_be_added)
        print("done")

    def getData(self): 
        print("reading submission data")
        with open(self.fname, 'r') as infile: 
            for line in infile:  
                data = self.getDataAtIndex(line)
                self.full_data_set.append(data)
        self.getTestData()

    def getDataAtIndex(self, line): 
        obj = next(self.decode_obj(line))
        data = pd.DataFrame.from_dict(obj['values'])
        return data

    def decode_obj(self, line, pos=0, decoder=JSONDecoder()):
        no_white_space_regex = re.compile(r'[^\s]')
        while True:
            match = no_white_space_regex.search(line, pos)
            if not match:
                return
            pos = match.start()
            try:
                obj, pos = decoder.raw_decode(line, pos)
            except JSONDecodeError as err:
                print("Oops! Something went wrong. Error : {}".format(err))
            yield obj

    def testCreature(self, creature, file_name): 
        creature_input = self.transformed_data 
        model = Neural_Network(creature.input_length, creature.hidden_length)
        model.setWeights(creature.getCreature()["weights"])
        predict = model.forward(torch.tensor(creature_input, dtype=torch.float))
        np_predict = np.asarray(predict[:,0] < predict[:,1], dtype=int)
        saved_file_name = file_name + ".csv"
        np.savetxt(saved_file_name, np_predict, delimiter=",")

    def getTransformedCreatureData(self): 
        full_data = self.test_set
        names = full_data.columns 
        aic_hold = []
        obs = len(full_data)/60
        one_percent = int(obs * .01)
        percent = 1
        min_row = 0 
        max_row = 60
        for x in range(0, int(obs)): 
            aic_row = []
            for index, name in enumerate(names): 
                parameter = self.time_mean_sd['ARIMA'][index]
                test_data = full_data[name][min_row:max_row]
                # with warnings.catch_warnings():
                #     warnings.simplefilter("ignore")
                #     model = tsmodel.ARIMA(test_data, (int(parameter[1]), int(parameter[4]), int(parameter[7])))
                #     aic = model.fit(disp=False).aic
                try: 
                    aic = self.arima(robjects.FloatVector(test_data), robjects.IntVector([int(parameter[1]), int(parameter[4]), int(parameter[7])]))[5][0] 
                except RRuntimeError:
                    aic = 0
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
            if x % one_percent is 0 and x is not 0: 
                print("{}%".format(percent))
                percent += 1
        self.transformed_data = np.array(aic_hold)