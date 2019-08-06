from json import JSONDecoder, JSONDecodeError

import numpy as np
import pandas as pd 
import re 
import random 
import os 

class TimeHelper(): 
    def __init__(self): 
        self.path_to_data = "D:/Dev/projects/georgiareu/bigdata2019-flare-prediction"
        self.file_name = ["fold1Training.json", "fold2Training.json", "fold3Training.json"]
        self.data_size = []
        self.training_set_size = 0
        self.training_set = []
        self.set_class_labels = []
        self.full_data_set = []
        self.solar_observations = []
        self.non_solar_observations = []
        self.getData()

    def getData(self): 
        non_count = 0 
        solar_count = 0 
        non_file_count = 0 
        solar_file_count = 0 
        non_solar_to_be_added = []
        solar_to_be_added = []
        for data_file in self.file_name: 
            fname = os.path.join(self.path_to_data, data_file)
            with open(fname, 'r') as infile: 
                for index, line in enumerate(infile):  
                    self.data_size.append(index)
                    data, class_label = self.getDataAtIndex(line)
                    if(data.isnull().values.any() == False): 
                        data.set_index(data.index.astype(int), inplace = True)
                        last_n_indices = np.arange(0, 60)
                        data = data.loc[last_n_indices]
                        if class_label is 0: 
                            non_solar_to_be_added.append(data)
                            non_count += 1 
                        else: 
                            solar_to_be_added.append(data)
                            solar_count += 1
                        if (non_count % 5000 is 0) and (non_count is not 0): 
                            non_name = "none_obs_" + str(non_file_count) + ".csv"
                            non_file_count += 1
                            non_count = 0 
                            pd.concat(non_solar_to_be_added).to_csv(non_name)
                            non_solar_to_be_added = []
                        if (solar_count % 5000 is 0) and (solar_count is not 0): 
                            solar_name = "solar_obs_" + str(solar_file_count) + ".csv"
                            solar_file_count += 1
                            solar_count = 0 
                            pd.concat(solar_to_be_added).to_csv(solar_name)
                            solar_to_be_added = []
        non_name = "none_obs_" + str(non_file_count) + ".csv"
        pd.concat(non_solar_to_be_added).to_csv(non_name)
        non_name = "none_obs_" + str(solar_file_count) + ".csv"
        pd.concat(non_solar_to_be_added).to_csv(non_name)

    def getTestData(self): 
        test_data_index = random.sample(self.data_size, self.training_set_size)
        test_frames_to_be_added = []
        self.set_class_labels = []
        for index in test_data_index: 
            data = self.full_data_set[index]["data"]
            class_label = self.full_data_set[index]["class_label"]
            if(data.isnull().values.any() == False): 
                data.set_index(data.index.astype(int), inplace = True)
                last_n_indices = np.arange(0, 60)
                data = data.loc[last_n_indices]
                test_frames_to_be_added.append(data)
                self.set_class_labels.append(class_label)
        self.training_set = pd.concat(test_frames_to_be_added)
        self.normalizeData()
        return self.training_set
                    
    def normalizeData(self): 
        normalized_data = self.training_set
        for name in normalized_data.columns:
            median = normalized_data[name].median()
            std = np.std(normalized_data[name])
            normalized_data[name] = (normalized_data[name] - median)/std
        self.training_set = normalized_data

    def getDataAtIndex(self, line): 
        obj = next(self.decode_obj(line))
        class_label = obj['classNum']
        data = pd.DataFrame.from_dict(obj['values'])
        return [data, class_label]
    
    def getClassTestData(self): 
        return(self.set_class_labels)

    def getDataSetSize(self): 
        return(self.data_size)

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