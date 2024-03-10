# import random
# from engine import Engine
# import os
# import pandas as pd
# import numpy as np
# class Generator(object):
#     def __init__(self,engine,folder_path,files):
#         self.folder_path = folder_path
#         self.train_files= files[0]
#         self.test_files= files[1]
#         self.engine= Engine(None)
#
#     def select_file(self):
#         file_test = random.choice(self.test_files)
#         print(f'file : {file_test}')
#         file_path = os.path.join(self.folder_path, file_test)
#         return file_path
#
#     def get_file_text(self,file_path):
#         return self.engine.get_text(file_path)
#
#     def get_merged_file(self):
#         merged_text=''
#         for file in self.test_files[:2]:
#             file_path = os.path.join(self.folder_path, file)
#             merged_text+= ' ' +self.engine.get_text(file_path)+' ' + '||'
#         return merged_text
#     def generate(self):
#         file_test= self.select_file()
#         text = self.get_file_text(file_test)
#         # merged_text= self.get_merged_file()
#         tokens = self.engine.tokenize(text,include_stopwords=True)
#         # tokens = self.engine.tokenize(merged_text,include_stopwords=True)
#         # print(f'text : {tokens}')
#         content=' '.join(tokens[:3])
#         start= ' '.join(tokens[:3])
#         next_words1_df= pd.read_csv('next_word1.csv')
#         next_words2_df= pd.read_csv('next_word2.csv')
#         next_words3_df= pd.read_csv('next_word3.csv')
#         for i in range (len(tokens)-3):
#             start=' '.join(tokens[i:i+3])
#             start_words = start.split()
#
#
#             # print('start --> ',start)
#
#             index3 = np.where(start==next_words3_df.iloc[:]['Token'])
#             index2 = np.where(start[:-1]==next_words2_df.iloc[:]['Token'])
#             index1 = np.where(start_words[-1] == next_words1_df.iloc[:]['Token'])
#             if (index3[0] and isinstance(next_words3_df.iloc[index3]['Most Common 1'].iloc[0],str)) : ## 3 to verify
#                 next_words3 = next_words3_df.iloc[index3]['Most Common 1'].iloc[0].split('|')[0]
#                 content+=' ' +next_words3
#                 # print(f'next_words3 : {next_words3}')
#             elif (index2[0]) : ## 2 to verify
#                 next_words2 = next_words2_df.iloc[index2]['Most Common 1'].iloc[0].split('|')[0]
#                 content+=' ' +next_words2
# #                 print(f'next_words2 : {next_words2}')
#
#
#             elif(index1[0]):
#
#                 next_words1 = next_words1_df.iloc[index1]['Most Common 1'].iloc[0].split('|')[0]
#                 content +=' ' +next_words1
# #                 print(f'next_words1 : {next_words1}')
#             else :
# #                 print('no matching ')
#                 content+=' '+ 'كلمة'
#         return [self.engine.tokenize(content,include_stopwords=True),self.engine.tokenize(text,include_stopwords=True)]
#
