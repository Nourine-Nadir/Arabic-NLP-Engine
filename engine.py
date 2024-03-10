# Import main libraries
import os
import pandas as pd
import numpy as np
import nltk
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from collections import defaultdict, Counter
import random
import sys
import string
import re

# Check if NLTK stopwords are already installed
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    # If not installed, download it
    nltk.download('stopwords')

    #Engine Class :
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
        self.train_files_=[]
        self.test_files_=[]


    def infos(self):
        words = self.extract_content(nb_files=6500, include_stopwords=False, sequence_size=1,print_details=True)
        df = pd.DataFrame(words, columns=['words'])
        print(df.describe())

        return df
    def get_text(self, file_path):
        # method to extract text from a file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            cleaned_text = self.remove_punctuation(text)# clean text of the file from punctuations
            return cleaned_text

    def remove_punctuation(self, text):
        # method to remove punctuation from the text
        allowed_chars = '\u0600-\u06FF' + string.whitespace  # Define allowed characters (arabic letters and whitespace)
        translator = str.maketrans('', '', ''.join(c for c in string.printable if c not in allowed_chars))
        cleaned_text = text.translate(translator)
        cleaned_text = re.sub(r"\s+", " ", cleaned_text)  # Replace multiple spaces with a single space

        return cleaned_text

    def extract_content(self, nb_files=None, include_stopwords=False, sequence_size=1,print_details=False):
        #method to loop through the folder after selecting random nb of files for training and testing

        nb_files = nb_files or self.total_nb_files # select all files if the number not specified
        all_files = os.listdir(self.folder_path)
        self.train_files_ = all_files[:nb_files] # get a random sample of files
        self.test_files_ = list(set(all_files) - set(self.train_files_)) # subtract from all files to get the remaining ones

        print(len(self.train_files_))
        content = ''
        i = 0
        if print_details:
            print(f'train_files= {len(self.train_files_)}')
            print(f'test_files= {len(self.test_files_)}')
            print(f'sequence_size= {sequence_size}')
        for filename in self.train_files_:
            if i == len(self.train_files_):
                break
            else:
                if filename.endswith('.txt'): # treat only .txt file type
                    file_path = os.path.join(self.folder_path, filename)
                    content += self.get_text(file_path)
            i += 1

        return self.tokenize(content, include_stopwords,sequence_size)

    def tokenize(self, text, include_stopwords=False, sequence_size=1):
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
        cleaned_tokens = [token for token in tokens if token.lower() not in self.stop_words and token.isalpha() and  not any(ord(char) < 128 for char in token) ]
        return cleaned_tokens

    def get_most_frequent_next_words(self, tokens,nb_next_words,token_len=None):

        print(f'nb of next words requested: {nb_next_words}')
        next_words_count = defaultdict(Counter) #instanciate a dict type obejct
        if token_len ==1:
            for i in range(len(tokens) - token_len):
                current_token = tokens[i] if isinstance(tokens[i], str) else ' '.join(tokens[i]) #check if the token is a single word or not
                next_word = tokens[i + 1] if isinstance(tokens[i + 1], str) else tokens[i + token_len]#check if the next word is a single word or not
                next_words_count[current_token].update([next_word]) # upadate the count of the next word or create it if not existing
            most_frequent_next_words = {}
        else:
            for i in range(len(tokens) - token_len):
                current_token = tokens[i] if isinstance(tokens[i], str) else ' '.join(tokens[i])  #check if the token is a single word or not
                next_word = tokens[i + 1] if isinstance(tokens[i + 1], str) else tokens[i + token_len]  #check if the next word is a single word or notz
                next_words_count[current_token].update(next_word)  # upadate the count of the next word or create it if not existing
            most_frequent_next_words = {}
        for token, counter in next_words_count.items():   # sort next words by descending order
            most_common = counter.most_common(nb_next_words)
            most_frequent_next_words[token] = most_common

        return most_frequent_next_words

    def dict_to_df(self, dictionary):

        data = []
        for token, common_words in dictionary.items():
            row = {'Token': token}
            for i, (word, count) in enumerate(common_words):
                row[f'Most Common {i + 1}'] = f'{word}|{count}'
            data.append(row)

        # Convert to DataFrame
        df = pd.DataFrame(data)
        return df
    def save_file(self, df,title):
        try:
            df.to_csv(title+'.csv', encoding='utf-8-sig', index=False)
            print('tokens file Saved !')
        except:
            print('Error saving file')

    #----GETTERS----
    def get_train_files(self):
        return  self.train_files_
    def get_test_files(self):
        return  self.test_files_

    def save_train_test_files(self):
        train_files_df=pd.DataFrame(columns=['Train_files'])
        test_files_df=pd.DataFrame(columns=['Test_files'])
        train_files_df['Train_files']=self.train_files_
        test_files_df['Test_files']=self.test_files_
        try:
            train_files_df.to_csv('train_test_files.csv', encoding='utf-8-sig', index=False)
            test_files_df.to_csv('test_test_files.csv', encoding='utf-8-sig', index=False)
            print('train test file Saved !')
        except:
            print('Error saving file')

    def select_file(self):
        file_test = random.choice(self.test_files_)
        print(f'file : {file_test}')
        file_path = os.path.join(self.folder_path, file_test)
        return file_path



    def get_merged_file(self):
        merged_text = ''
        for file in self.test_files_[:2]:
            file_path = os.path.join(self.folder_path, file)
            merged_text += ' ' + self.get_text(file_path) + ' ' + '||'
        return merged_text

    def generate(self):
        file_test = self.select_file()
        text = self.get_text(file_test)
        # merged_text= self.get_merged_file()
        tokens = self.tokenize(text, include_stopwords=True)
        # tokens = self.tokenize(merged_text,include_stopwords=True)
        # print(f'text : {tokens}')
        content = ' '.join(tokens[:3])
        start = ' '.join(tokens[:3])
        next_words1_df = pd.read_csv('next_word1.csv')
        next_words2_df = pd.read_csv('next_word2.csv')
        next_words3_df = pd.read_csv('next_word3.csv')
        for i in range(len(tokens) - 3):
            start = ' '.join(tokens[i:i + 3])
            start_words = start.split()

            # print('start --> ',start)

            index3 = np.where(start == next_words3_df.iloc[:]['Token'])
            index2 = np.where(start[:-1] == next_words2_df.iloc[:]['Token'])
            index1 = np.where(start_words[-1] == next_words1_df.iloc[:]['Token'])
            if (index3[0] and isinstance(next_words3_df.iloc[index3]['Most Common 1'].iloc[0],
                                         str)):  ## 3 to verify
                next_words3 = next_words3_df.iloc[index3]['Most Common 1'].iloc[0].split('|')[0]
                content += ' ' + next_words3
                # print(f'next_words3 : {next_words3}')
            elif (index2[0]):  ## 2 to verify
                next_words2 = next_words2_df.iloc[index2]['Most Common 1'].iloc[0].split('|')[0]
                content += ' ' + next_words2
            #                 print(f'next_words2 : {next_words2}')

            elif (index1[0]):

                next_words1 = next_words1_df.iloc[index1]['Most Common 1'].iloc[0].split('|')[0]
                content += ' ' + next_words1
            #                 print(f'next_words1 : {next_words1}')
            else:
                #                 print('no matching ')
                content += ' ' + 'كلمة'
        return [self.tokenize(content, include_stopwords=True),
                self.tokenize(text, include_stopwords=True)]


