from farasapy.farasa.ner import FarasaNamedEntityRecognizer
import pandas as pd
NER = FarasaNamedEntityRecognizer()

df=pd.read_csv('NLP TP/syntax_verification_results.csv')
incorrect_words= df['Incorrect words']
incorrect_words.dropna(inplace=True)

result = NER.recognize(' '.join(incorrect_words.values))
res = result.split(' ')
#
NER_df=pd.DataFrame(res)
NER_df.to_csv('NLP TP/NER_DF.csv', encoding='utf-8-sig')
result = NER_df.map(lambda x: x.split('/'))


res= [value for list in result.values for value in list if value[-1]=='O']
res=pd.DataFrame(res)
res = res.rename(columns={0: 'word', 1: 'type'})
res.set_index('word', inplace=True)
res.to_csv('NLP TP/NER_FILTERED.csv', encoding='utf-8-sig')