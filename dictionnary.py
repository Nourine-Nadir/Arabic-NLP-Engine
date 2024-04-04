import json
import numpy as np
import os

import pandas as pd

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

    def verify_syntax(self,print_details= False,save_file=True):
        print('Checking syntax')
        dictionary_set = set(self.dictionary_words_) # for a faster treatment (Sets have constant time complexity for membership tests)

        self.correct_words_list = []
        self.incorrect_words_list = []
        unique_tokens = np.unique(self.tokens)
        for word in self.tokens:
            if word in dictionary_set:
                self.correct_words_list.append(word)
            else:
                self.incorrect_words_list.append(word)
        if print_details:
            print(f'Correct words {len(self.correct_words_list)} \nIncorrect words {len(self.incorrect_words_list)}')

        with open('incorrect_words.txt', 'w', encoding="utf-8-sig") as f:
            f.write('\n'.join(self.incorrect_words_list))
        self.save_to_file()
        return
    def save_to_file(self):
        max_len=max(len(self.incorrect_words_list), len(self.correct_words_list))
        df = pd.DataFrame({'Incorrect words': [np.nan]*max_len, 'Correct words': [np.nan]*max_len})
        df['Incorrect words'] = df['Incorrect words'].astype('object')
        df['Correct words'] = df['Correct words'].astype('object')

        df.loc[:len(self.incorrect_words_list)- 1,'Incorrect words']=self.incorrect_words_list
        df.loc[:len(self.correct_words_list)- 1,'Correct words']=self.correct_words_list

        df.to_csv('syntax_verification_results.csv',encoding='utf-8-sig',index=False)


