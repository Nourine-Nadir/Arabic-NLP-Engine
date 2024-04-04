import pandas as pd
import numpy as np
from farasapy.farasa.stemmer import FarasaStemmer

class Lemmatizer(object):
    def __init__(self):
        self.farasa_lemmatizer = FarasaStemmer(interactive=True)
        self.words_=[]
        self.lemmatized_words_=[]
    def lemmatize(self,words,save_file=True):
        self.words_=np.unique(words)
        # Lemmatize each token
        self.lemmatized_words_ = [self.farasa_lemmatizer.stem(token) for token in self.words_]

        self.save_lemmatized_words()
        return self.lemmatized_words_

    def save_lemmatized_words(self):
        df=pd.DataFrame()
        df['words']=self.words_
        df['lemmatized_words']=self.lemmatized_words_
        try:
            df.to_csv('lemmatized_words.csv', encoding='utf-8-sig', index=False)
            print('lemmatized file Saved !')
        except:
            print('Error saving file')
