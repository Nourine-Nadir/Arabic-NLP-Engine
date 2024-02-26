import pandas as pd

from farasapy.farasa.stemmer import FarasaStemmer

class Lemmatizer(object):
    def __init__(self):
        self.farasa_lemmatizer = FarasaStemmer(interactive=True)
        self.words_=[]
        self.lemmatized_words_=[]
    def lemmatize(self,words):
        self.words_=words
        # Lemmatize each token
        lemmatized_words = [self.farasa_lemmatizer.stem(token) for token in words]
        len(lemmatized_words)

        for word, lemmatized_word in zip(words[:50], lemmatized_words[:50]):
            print(f"Original Word: {word.split()}, Lemmatized Word: {lemmatized_word}")
            self.lemmatized_words_=lemmatized_words
        return lemmatized_words

    def save_lemmatized_words(self):
        df=pd.DataFrame()
        df['words']=self.words_
        df['lemmatized_words']=self.lemmatized_words_
        try:
            df.to_csv('lemmatized_words.csv', encoding='utf-8-sig', index=False)
            print('file Saved !')
        except:
            print('Error saving file')
