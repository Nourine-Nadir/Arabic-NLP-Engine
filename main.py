import numpy as np
from evaluate import Evaluator
from engine import Engine
from dictionnary import Dictionary
from lemmatizer import Lemmatizer
from tqdm import tqdm

data_path = 'NLP arabic data/Sports'
nb_files = 6450

# #----------------ENGINE------------------
engine = Engine(data_path,nb_files=nb_files)  # instantiate the engine object


# words_df = engine.infos()
tokens = []
for sequence_size in [1, 2, 3]:
  tokens.append(engine.extract_content(include_stopwords=True, sequence_size=sequence_size, print_details=True))

next_words = {}  # Assuming you want a dictionary to store next words
# for i, token_list in enumerate(tokens):
#   title = f"next_word{i+1}"  # Generate title based on loop index
#   next_words[title] = engine.get_most_frequent_next_words(tokens=token_list, nb_next_words=3, token_len=i+1, save_file=True, title=title)
#
# engine.save_train_test_files()
# ----------------LEMMATIZER----------------

lemmatizer = Lemmatizer()
lemmatized_words= lemmatizer.lemmatize(tokens[0],save_file=True)

#--------------DICTIONARY---------------
#
dict_path = "arabic dictionary"
dictionary = Dictionary(dict_path,lemmatized_words,nb_files)
dicts = dictionary.get_dictionaries()
arabic_words = dictionary.get_data(dicts)
dictionary.verify_syntax(save_file=True)
#
# # --------------GENERATOR & EVALUATOR---------------
#
# evaluator = Evaluator()
# print(f'test : {engine.test_files_}')
# for file in tqdm(engine.test_files_):
#     generated_text, original_text = engine.generate_by_dist(file)
#     evaluator.evaluate(original_text, generated_text)
#
# print(f'avg score : {(evaluator.accumualted_score / len(engine.test_files_)) * 100}%')
