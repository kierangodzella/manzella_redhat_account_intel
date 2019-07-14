# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 01:14:37 2019

@author: kiera
"""

import pandas as pd

class PreProcessing(object):
    def __init__(self, data):
        self.data = data

    def _preprocess(self):
        df = self.data
        keycols = ['genres','budget','gross','director_name']
        for col in keycols:
            df = df[df[col].notnull()]
        df = df[['genres','budget','gross','director_name','actor_1_name',
                 'actor_2_name','actor_3_name','imdb_score']]
        df['ROI'] = (df.gross - df.budget) / df.budget
        df['net'] = df.gross - df.budget
        df_1hot = df.drop('genres',1).join(df.genres.str.get_dummies())
        
        genres_all = pd.Series(df.genres).unique()
        genres_list = []
        for item in genres_all:
            genres_list.append(item.split('|'))
        genres_values = list(set(
                [item for sublist in genres_list for item in sublist])) 
        
        unique_directors = list(set(list(pd.Series(df.director_name).unique())))
        
        self.processed_data = df_1hot
        self.genres = genres_values
        self.directors = unique_directors
    
    def _run(self):
        self._preprocess()
        return (self.processed_data, self.genres, self.directors)