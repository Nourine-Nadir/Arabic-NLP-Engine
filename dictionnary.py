import json
import numpy as np
import os
# --------------------Dictionary Class --------------------
class Dictionary(object):
    def __init__(self,path):
        self.folder_path = path

    def get_dictionaries (self):
        json_files = [file for file in os.listdir(self.folder_path) if file.endswith(".json")]

        dicts = []
        # Loop through each files
        for json_file in json_files:
            file_path = os.path.join(self.folder_path, json_file)
            with open(file_path, "r", encoding="utf-8") as f:
                dicts.append(json.load(f))

        return dicts
    def get_data(self,dicts):
        data = []
        for dict in dicts:
            for key in dict:
                for key2 in dict[key]:
                    data.extend(dict[key][key2])
        return data

    def verify_syntax(self,dictionary_words,data):
        print('Cheking syntax')
        dictionary_set = set(dictionary_words) # for a faster treatment (Sets have constant time complexity for membership tests)
        correct_words = 0
        wrong_words = 0
        for word in data:
            if word in dictionary_set:
                correct_words += 1
            else:
                wrong_words += 1
        return [correct_words, wrong_words]
# --------------------MAIN--------------------
# folder_path = "NLP arabic data"
#
# dictionary = Dictionary(folder_path)
# dicts = dictionary.get_dictionaries()
# data = dictionary.get_data(dicts)
#
#
# print(f'data length {len((data))}')
# unique_data= np.unique(data)
# print(f'unique data length {len(unique_data)}')
