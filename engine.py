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
from tqdm import tqdm
import csv
import json

# Check if NLTK stopwords are already installed
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    # If not installed, download it
    nltk.download('stopwords')

    # Engine Class :


class Engine(object):
    def __init__(self, path, nb_files):
        self.folder_path = path
        try:
            self.total_nb_files = len(os.listdir(self.folder_path))  # Get the number of files in the folder
            print('Files loaded with success')
        except:
            print('Files not found')
            sys.exit(1)
        # Get the Arabic stop words
        self.stop_words = list(stopwords.words('arabic'))  # NLTK arabic stopwords

        nb_files = nb_files or self.total_nb_files  # select all files if the number not specified
        all_files = os.listdir(self.folder_path)
        self.train_files_ = random.sample(all_files, nb_files)
        self.test_files_ = list(set(all_files) - set(self.train_files_))
        self.import_files()

    def import_files(self):
        try:
            self.next_words1_df = pd.read_csv('next_word1.csv')
            self.next_words1_df = self.next_words1_df.set_index('Token')

        except FileNotFoundError:
            self.next_words1_df = pd.DataFrame()
        try:
            self.next_words2_df = pd.read_csv('next_word2.csv')
            self.next_words2_df = self.next_words2_df.set_index('Token')

        except FileNotFoundError:
            self.next_words2_df = pd.DataFrame()
        try:
            self.next_words3_df = pd.read_csv('next_word3.csv')
            self.next_words3_df = self.next_words3_df.set_index('Token')

        except FileNotFoundError:
            self.next_words3_df = pd.DataFrame()

    def infos(self):
        words = self.extract_content(nb_files=6500, include_stopwords=False, sequence_size=1, print_details=True)
        df = pd.DataFrame(words, columns=['words'])
        print(df.describe())

        return df

    def get_text(self, file_path):
        # method to extract text from a file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            cleaned_text = self.remove_punctuation(text)  # clean text of the file from punctuations
            return cleaned_text

    def remove_punctuation(self, text):
        # method to remove punctuation from the text
        allowed_chars = '\u0600-\u06FF' + string.whitespace  # Define allowed characters (arabic letters and whitespace)
        translator = str.maketrans('', '', ''.join(c for c in string.printable if c not in allowed_chars))
        cleaned_text = text.translate(translator)
        cleaned_text = re.sub(r"\s+", " ", cleaned_text)  # Replace multiple spaces with a single space

        return cleaned_text

    def extract_content(self, nb_files=None, include_stopwords=False, sequence_size=1, print_details=False):

        content = ''
        i = 0
        if print_details:
            print(f'train_files= {len(self.train_files_)}')
            print(f'test_files= {len(self.test_files_)}')
            print(f'sequence_size= {sequence_size}')
        for filename in tqdm(self.train_files_):
            if i == len(self.train_files_):
                break
            else:
                if filename.endswith('.txt'):  # treat only .txt file type
                    file_path = os.path.join(self.folder_path, filename)
                    content += self.get_text(file_path)
            i += 1

        return self.tokenize(content, include_stopwords, sequence_size)

    def tokenize(self, text, include_stopwords=False, sequence_size=1):
        ## private method to tokenize content extracted from all files
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(text)

        if sequence_size == 1:
            # individual tokens
            if include_stopwords:
                return tokens
            else:
                # if include_stopwords = False => clean tokens
                cleaned_tokens = self.__clean_tokens(tokens)
                return cleaned_tokens
        else:
            # tokenize by sequences of 2 or more words
            sequences = [tuple(tokens[i:i + sequence_size]) for i in range(len(tokens) - sequence_size + 1)]
            if include_stopwords:
                return sequences
            else:
                # if include_stopwords = False => clean sequences
                cleaned_sequences = [self.__clean_tokens(seq) for seq in sequences]
                return cleaned_sequences

    def __clean_tokens(self, tokens):
        cleaned_tokens = [token for token in tokens if
                          token.lower() not in self.stop_words and token.isalpha() and not any(
                              ord(char) < 128 for char in token)]
        return cleaned_tokens

    def get_most_frequent_next_words(self, tokens, nb_next_words, token_len=None, title=None, save_file=True):

        print(f'nb of next words requested: {nb_next_words}')
        next_words_count = defaultdict(Counter)  # instanciate a dict type obejct
        if token_len == 1:
            for i in range(len(tokens) - token_len):
                current_token = tokens[i] if isinstance(tokens[i], str) else ' '.join(
                    tokens[i])  # check if the token is a single word or not
                next_word = tokens[i + 1] if isinstance(tokens[i + 1], str) else tokens[
                    i + token_len]  # check if the next word is a single word or not
                next_words_count[current_token].update(
                    [next_word])  # upadate the count of the next word or create it if not existing
            most_frequent_next_words = {}
        else:
            for i in range(len(tokens) - token_len):
                current_token = tokens[i] if isinstance(tokens[i], str) else ' '.join(
                    tokens[i])  # check if the token is a single word or not
                next_word = tokens[i + 1] if isinstance(tokens[i + 1], str) else tokens[
                    i + token_len]  # check if the next word is a single word or notz
                next_words_count[current_token].update(
                    next_word)  # upadate the count of the next word or create it if not existing
            most_frequent_next_words = {}
        for token, counter in next_words_count.items():  # sort next words by descending order
            most_common = counter.most_common(nb_next_words)
            most_frequent_next_words[token] = most_common

        if save_file:
            next_word_df = self.dict_to_df(most_frequent_next_words)  # transform next words dict to pandas DataFrame
            self.save_file(next_word_df, title)  # save the dataFrame into a .csv file

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

    def save_file(self, df, title):
        try:
            df.to_csv(title + '.csv', encoding='utf-8-sig', index=False)
            # self.csv_to_json(csv_file=title + '.csv', json_file=title + '.json')
            self.import_files()
            print('tokens file Saved !')

        except:
            print('Error saving tokens file')

    def csv_to_json(self, csv_file, json_file):

        with open(csv_file, 'r', encoding='utf-8-sig') as csvfile, open(json_file, 'w',
                                                                        encoding='utf-8-sig') as jsonfile:
            reader = csv.DictReader(csvfile)
            data = []
            for row in reader:
                data.append(row)

            json.dump(data, jsonfile, ensure_ascii=False, indent=2)  # Add indentation for readability

    # ----GETTERS----
    def get_train_files(self):
        return self.train_files_

    def get_test_files(self):
        return self.test_files_

    def save_train_test_files(self):
        train_files_df = pd.DataFrame(columns=['Train_files'])
        test_files_df = pd.DataFrame(columns=['Test_files'])
        train_files_df['Train_files'] = self.train_files_
        test_files_df['Test_files'] = self.test_files_
        try:
            train_files_df.to_csv('train_files.csv', encoding='utf-8-sig', index=False)
            test_files_df.to_csv('test_files.csv', encoding='utf-8-sig', index=False)
            print('train test file Saved !')
        except:
            print('Error saving file')

    def select_file(self, file):
        file_test = file
        # print(f'file : {file_test}')
        file_path = os.path.join(self.folder_path, file_test)
        return file_path

    def generate_best(self, file):
        file_test = self.select_file(file)
        text = self.get_text(file_test)
        tokens = self.tokenize(text, include_stopwords=True)
        content = ' '.join(tokens[:3])
        start = ' '.join(tokens[:3])

        for i in range(len(tokens) - 3):
            start = ' '.join(tokens[i:i + 3])
            start_words = start.split()

            # print('start --> ',start)

            index3 = start in self.next_words3_df.index  # Check if start exists as index
            index2 = start[:-1] in self.next_words2_df.index  # Check if start[:-1] exists as index
            index1 = start_words[-1] in self.next_words1_df.index  # Check if start_words[-1] exists as index
            # print(index3, index2, index1)
            if index3 and isinstance(self.next_words3_df.loc[start, 'Most Common 1'], str):
                ## 3 to verify
                next_words3, freq = self.next_words3_df.loc[start, 'Most Common 1'].split('|')
                content += ' ' + next_words3
            elif (index2):  ## 2 to verify
                next_words2, freq = self.next_words2_df.loc[start[:-1], 'Most Common 1'].split('|')
                content += ' ' + next_words2

            elif (index1):

                next_words1, freq = self.next_words1_df.loc[start_words[-1], 'Most Common 1'].split('|')
                content += ' ' + next_words1
            else:
                #                 print('no matching ')
                content += ' ' + 'كلمة'
        return [self.tokenize(content, include_stopwords=True),
                self.tokenize(text, include_stopwords=True)]

    def generate_by_dist(self, file):
        file_test = self.select_file(file)
        text = self.get_text(file_test)
        tokens = self.tokenize(text, include_stopwords=True)
        content = ' '.join(tokens[:3])
        start = ' '.join(tokens[:3])

        for i in range(len(tokens) - 3):
            start = ' '.join(tokens[i:i + 3])
            start_words = start.split()

            # print('start --> ',start)

            index3 = start in self.next_words3_df.index  # Check if start exists as index
            index2 = start[:-1] in self.next_words2_df.index  # Check if start[:-1] exists as index
            index1 = start_words[-1] in self.next_words1_df.index  # Check if start_words[-1] exists as index
            if (index3):
                print(f'start : {start}')
                possible_words = []
                frequencies = []
                for value in self.next_words3_df.loc[start, :]:
                    if isinstance(value, str):
                        print(f'word : {value}')
                        word, freq = value.split('|')
                        possible_words.append(word)
                        frequencies.append(int(freq))
                print(f'possible_words {possible_words} \n freq {frequencies}')

                next_words = random.choices(possible_words, weights=frequencies)[0]
                print(f'next_words {next_words}')
                content += ' ' + next_words
            elif (index2):
                print(f'start : {start[:-1]}')
                possible_words = []
                frequencies = []
                for value in self.next_words2_df.loc[start[:-1], :]:
                    if isinstance(value, str):
                        print(f'word : {value}')
                        word, freq = value.split('|')
                        possible_words.append(word)
                        frequencies.append(int(freq))
                print(f'possible_words {possible_words} \n freq {frequencies}')

                next_words = random.choices(possible_words, weights=frequencies)[0]
                print(f'next_words {next_words}')
                content += ' ' + next_words
            elif (index1):
                print(f'start : {start_words[-1]}')
                possible_words = []
                frequencies = []
                for value in self.next_words1_df.loc[start_words[-1], :]:
                    if isinstance(value, str):
                        print(f'word : {value}')
                        word, freq = value.split('|')
                        possible_words.append(word)
                        frequencies.append(int(freq))
                print(f'possible_words {possible_words} \n freq {frequencies}')

                next_words = random.choices(possible_words, weights=frequencies)[0]
                print(f'next_words {next_words}')
                content += ' ' + next_words
            else:
                #                 print('no matching ')
                content += ' ' + 'كلمة'
        return [self.tokenize(content, include_stopwords=True),
                self.tokenize(text, include_stopwords=True)]
