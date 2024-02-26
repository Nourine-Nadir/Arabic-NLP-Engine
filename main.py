import numpy as np

from engine import Engine
from dictionnary import Dictionary
from lemmatizer import Lemmatizer
import seaborn as sns

data_path= 'NLP arabic data/Sports'
nb_files=6000
#----------------ENGINE------------------
engine = Engine(data_path) # instantiate the engine object
tokens = engine.extract_content(nb_files=nb_files, include_stopwords=False,sequence_size=1,print_details=True) # extract tokens
unique_tokens = np.unique(tokens)

###-----NEXT WORDS------
next_words = engine.get_most_frequent_next_words(tokens, nb_next_words=10) # get token next words(sequences)
next_word_df = engine.dict_to_df(next_words) # transform next words dict to pandas DataFrame
engine.save_file(next_word_df) # save the dataFrame into a .csv file

#----------------LEMMATIZER----------------
lemmatizer = Lemmatizer()
lemmatized_words= lemmatizer.lemmatize(unique_tokens)

lemmatizer.save_lemmatized_words()
#--------------DICTIONARY---------------
dict_path = "arabic dictionary"
dictionary = Dictionary(dict_path,lemmatized_words,nb_files)
dicts = dictionary.get_dictionaries()
arabic_words = dictionary.get_data(dicts)

dictionary.verify_syntax()

# print(dictionary.correct_words_)
# print(dictionary.incorrect_words_)

