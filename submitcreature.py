from json import JSONDecoder, JSONDecodeError

from neuralnetwork import Neural_Network

import pandas as pd
import numpy as np

import os
import re
import json
import torch

class SubmitCreature(): 
    def __init__(self): 
        self.path_to_data = "D:/Dev/projects/georgiareu/bigdata2019-flare-prediction"
        self.file_name = "testSet.json"
        self.fname = os.path.join(self.path_to_data, self.file_name)
        self.full_data_set = []
        self.test_set = []
        self.getData()

    def getTestData(self): 
        test_frames_to_be_added = []
        for data in self.full_data_set: 
            data.set_index(data.index.astype(int), inplace = True)
            last_n_indices = np.arange(0, 60)
            data = data.loc[last_n_indices]
            test_frames_to_be_added.append(data)
        self.test_set = pd.concat(test_frames_to_be_added)
        self.normalizeData()

    def normalizeData(self): 
        normalized_data = self.test_set
        for name in normalized_data.columns:
            median = normalized_data[name].median()
            std = np.std(normalized_data[name])
            normalized_data[name] = (normalized_data[name] - median)/std
        self.test_set = normalized_data


    def getData(self): 
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
        creature_test_data = self.getTransformedCreatureData(creature)
        creature_test_data = np.array(creature_test_data)
        creature_test_data = np.transpose(creature_test_data)
        model = Neural_Network(creature["input_length"], creature["hidden_length"])
        model.setWeights(creature["weights"])
        predict = model.forward(torch.tensor(creature_test_data, dtype=torch.float))
        np_predict = np.asarray(predict[:,0] < predict[:,1], dtype=int)
        saved_file_name = file_name + ".csv"
        np.savetxt(saved_file_name, np_predict, delimiter=",")

    def getTransformedCreatureData(self, creature): 
        col_names = True
        column_names = []
        transformed_data = []
        creature_genome = creature["genome"]
        for gene in creature_genome: 
            gene_min_index = gene['min']
            gene_max_index = gene['max']
            gene_name = gene['name']
            for index in range(gene_min_index, gene_max_index+1): 
                gene_data = pd.DataFrame(self.test_set[gene_name][index]).transpose()
                if(col_names): 
                    for col_index in range(0, gene_data.shape[1]): 
                        column_names.append(col_index)
                    col_names = False
                gene_data.columns = column_names
                transformed_data.append(gene_data)
        return(pd.concat(transformed_data)) 