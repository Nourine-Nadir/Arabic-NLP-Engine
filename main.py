import numpy as np
from evaluate import Evaluator

from engine import Engine
from dictionnary import Dictionary
from lemmatizer import Lemmatizer

data_path= 'NLP arabic data/Sports'
nb_files=6450

# #----------------ENGINE------------------
engine = Engine(data_path)   # instantiate the engine object

tokens_1 = engine.extract_content(nb_files=nb_files,
                                  include_stopwords=True,
                                  sequence_size=1,
                                  print_details=True)   # extract tokens
# engine.save_train_test_files()
# words_df = engine.infos()
# words_df.head()
tokens_2 = engine.extract_content(nb_files=nb_files,
                                  include_stopwords=True,
                                  sequence_size=2,
                                  print_details=True)   # extract tokens
tokens_3 = engine.extract_content(nb_files=nb_files,
                                  include_stopwords=True,
                                  sequence_size=3,
                                  print_details=True)   # extract tokens
#
# ##-----NEXT WORDS 1token------
next_words = engine.get_most_frequent_next_words(tokens_1, nb_next_words=1, token_len=1)   # get token next words(sequences)
next_word_df = engine.dict_to_df(next_words) # transform next words dict to pandas DataFrame
engine.save_file(next_word_df,'next_word1') # save the dataFrame into a .csv file
##-----NEXT WORDS 2tokens------
next_words2 = engine.get_most_frequent_next_words(tokens_2, nb_next_words=1, token_len=2)   # get token next words(sequences)
next_word2_df = engine.dict_to_df(next_words2) # transform next words dict to pandas DataFrame
engine.save_file(next_word2_df,'next_word2') # save the dataFrame into a .csv file

##-----NEXT WORDS 3tokens------
next_words3 = engine.get_most_frequent_next_words(tokens_3, nb_next_words=1, token_len=3)   # get token next words(sequences)
next_word3_df = engine.dict_to_df(next_words3)  # transform next words dict to pandas DataFrame
engine.save_file(next_word3_df,'next_word3')   # save the dataFrame into a .csv file

#----------------LEMMATIZER----------------
# lemmatizer = Lemmatizer()
# unique_words = np.unique(tokens_1)
# lemmatized_words= lemmatizer.lemmatize(unique_words)
#
# lemmatizer.save_lemmatized_words()
# #--------------DICTIONARY---------------
# dict_path = "arabic dictionary"
# dictionary = Dictionary(dict_path,lemmatized_words,nb_files)
# dicts = dictionary.get_dictionaries()
# arabic_words = dictionary.get_data(dicts)
#
# dictionary.verify_syntax()
# dictionary.save_to_file()
#
# #--------------GENERATOR & EVALUATOR---------------
evaluator = Evaluator()

train_files= engine.get_train_files()
test_files=  engine.get_test_files()
for file in test_files[:5]:
    generated_text,original_text = engine.generate()
    evaluator.evaluate(original_text, generated_text)

print(f'avg score : {(evaluator.accumualted_score/5)*100}%')
