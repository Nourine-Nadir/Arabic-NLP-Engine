import json
import numpy as np
import os
from engine import Engine

# --------------------Dictionary Class --------------------
class Dictionary(object):
    def __init__(self,dict_path,tokens,nb_files):
        self.dict_folder_path = dict_path
        self.tokens = tokens  # extract corpus words
        self.dictionary_words_ = []
        self.correct_words_=[]
        self.incorrect_words_=[]
    def get_dictionaries (self):
        json_files = [file for file in os.listdir(self.dict_folder_path) if file.endswith(".json")]

        dicts = []
        # Loop through each files
        for json_file in json_files:
            file_path = os.path.join(self.dict_folder_path, json_file)
            with open(file_path, "r", encoding="utf-8") as f:
                dicts.append(json.load(f))

        return dicts
    def get_data(self,dicts):
        data = []
        for dict in dicts:
            for key in dict:
                for key2 in dict[key]:
                    data.extend(dict[key][key2])
        self.dictionary_words_ = np.unique(data)
        return self.dictionary_words_

    def verify_syntax(self,print_details=True):
        print('Checking syntax')
        dictionary_set = set(self.dictionary_words_) # for a faster treatment (Sets have constant time complexity for membership tests)
        correct_words = 0
        incorrect_words = 0
        correct_words_list = []
        incorrect_words_list = []
        unique_tokens = np.unique(self.tokens)
        for word in self.tokens:
            if word in dictionary_set:
                correct_words += 1
            else:
                incorrect_words_list.append(word)
                incorrect_words += 1
        if print_details:
            print(f'Correct words {correct_words} \nIncorrect words {incorrect_words}')
        print(incorrect_words_list[:3])
        with open('incorrect_words.txt', 'w', encoding="utf-8-sig") as f:
            f.write('\n'.join(incorrect_words_list))

        self.correct_words_=correct_words
        self.incorrect_words_=incorrect_words
        return
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
