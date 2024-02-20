from engine import Engine
from dictionnary import Dictionary
import pandas as pd
import numpy as np

folder_path='NLP arabic data/Sports'
nb_files=6000
engine = Engine(folder_path) # instantiate the engine object
tokens = engine.extract_content(nb_files=nb_files, include_stopwords=True,sequence_size=2) # extract tokens
next_words = engine.get_most_frequent_next_words(tokens, nb_next_words=10) # get token next words(sequences)
next_word_df = engine.dict_to_df(next_words) # transform next words dict to pandas DataFrame
engine.save_file(next_word_df) # save the dataFrame into a .csv file


tokens = engine.extract_content( include_stopwords=False,sequence_size=1) # extract corpus words

folder_path = "arabic dictionary"
dictionary = Dictionary(folder_path)
dicts = dictionary.get_dictionaries()
arabic_words = dictionary.get_data(dicts)

unique_arabic_words= np.unique(arabic_words)
# print(f'unique arabic_words length {len(unique_arabic_words)}')

correct_words,incorrect_words =dictionary.verify_syntax(unique_arabic_words,tokens)

print(f'Correct words {correct_words} \nIcorrect words {incorrect_words}')