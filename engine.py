# Import main libraries
import os
import pandas as pd
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from collections import defaultdict, Counter
import random
import sys
import string

# Engine Class :
class Engine(object):
    def __init__(self, path):
        self.folder_path = path
        try:
            self.total_nb_files = len(os.listdir(self.folder_path)) # Get the number of files in the folder
            print('Files loaded with success')
        except :
            print('Files not found')
            sys.exit(1)
        # Get the Arabic stop words
        self.stop_words = list(stopwords.words('arabic')) # NLTK arabic stopwords

    def get_text(self, file_path):
        # method to extract text from a file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            cleaned_text = self.remove_punctuation(text)# clean text of the file from punctuations
            return cleaned_text

    def remove_punctuation(self, text):
        # method to remove punctuation from the text
        translator = str.maketrans("", "", string.punctuation)
        cleaned_text = text.translate(translator)
        return cleaned_text

    def extract_content(self, nb_files=None, include_stopwords=False, sequence_size=1):
        #method to loop through the folder after selecting random nb of files for training and testing

        nb_files = nb_files or self.total_nb_files # select all files if the number not specified
        all_files = os.listdir(self.folder_path)
        train_files = random.sample(all_files, nb_files) # get a random sample of files
        test_files = list(set(all_files) - set(train_files)) # subtract from all files to get the remaining ones

        content = ''
        i = 0
        print(f'train_files= {len(train_files)}')
        print(f'test_files= {len(test_files)}')
        print(f'sequence_size= {sequence_size}')
        for filename in train_files:
            if i == nb_files:
                break
            else:
                if filename.endswith('.txt'): # treat only .txt file type
                    file_path = os.path.join(self.folder_path, filename)
                    content += self.get_text(file_path)
            i += 1

        return self.__tokenize(content, include_stopwords,sequence_size)

    def __tokenize(self, text, include_stopwords, sequence_size=1):
        ## private method to tokenize content extracted from all files
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(text)

        if sequence_size == 1:
            #individual tokens
            if include_stopwords:
                return tokens
            else:
                # if include_stopwords = False => clean tokens
                cleaned_tokens = self.__clean_tokens(tokens)
                return cleaned_tokens
        else:
            #tokenize by sequences of 2 or more words
            sequences = [tuple(tokens[i:i + sequence_size]) for i in range(len(tokens) - sequence_size + 1)]
            if include_stopwords:
                return sequences
            else:
                # if include_stopwords = False => clean sequences
                cleaned_sequences = [self.__clean_tokens(seq) for seq in sequences]
                return cleaned_sequences

    def __clean_tokens(self, tokens):
        cleaned_tokens = [token for token in tokens if token.lower() not in self.stop_words and token.isalpha()]
        return cleaned_tokens

    def get_most_frequent_next_words(self, tokens,nb_next_words):

        print(f'nb of next words requested: {nb_next_words}')
        next_words_count = defaultdict(Counter) #instanciate a dict type obejct

        for i in range(len(tokens) - 1):
            current_token = tokens[i] if isinstance(tokens[i], str) else ' '.join(tokens[i]) #check if the token is a single word or not
            next_word = tokens[i + 1] if isinstance(tokens[i + 1], str) else ' '.join(tokens[i + 1])#check if the next word is a single word or not
            next_words_count[current_token].update([next_word]) # upadate the count of the next word or create it if not existing

        most_frequent_next_words = {}
        for token, counter in next_words_count.items(): # sort next words by descending order
            most_common = counter.most_common(nb_next_words)
            most_frequent_next_words[token] = most_common

        return most_frequent_next_words

    def dict_to_df(self, dictionary):

        data = []
        for token, common_words in dictionary.items():
            row = {'Token': token}
            for i, (word, count) in enumerate(common_words):
                row[f'Most Common {i + 1}'] = f'{word} ({count})'
            data.append(row)

        # Convert to DataFrame
        df = pd.DataFrame(data)
        return df
    def save_file(self, df):
        try:
            df.to_csv('next_words.csv', encoding='utf-8-sig', index=False)
            print('file Saved !')
        except:
            print('Error saving file')
