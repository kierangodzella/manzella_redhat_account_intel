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
        
        # bring in data from self, and start manipulation by excluding rows
        # that are missing key values for the question we're trying to answer
        # and then selecting a subset with those variables. You could do the 
        # subselection first and then dropna(), this way but cols can be 
        # selected or excluded if other calculations need to be made
        keycols = ['genres','budget','gross','director_name']
        for col in keycols:
            df = df[df[col].notnull()]
        df = df[['genres','budget','gross','director_name']]
        
        # make two new columns for ROI and net, and one-hot encode each film
        # for the genres it is a member of. one film can be in multiple genres,
        # and pandas does a wonderful job splitting up those variables
        df['ROI'] = (df.gross - df.budget) / df.budget
        df['net'] = df.gross - df.budget
        df_1hot = df.drop('genres',1).join(df.genres.str.get_dummies())
        
        # the dataframe is already where we need it to be, but these lists of
        # unique genres and directors will help in the ranking function of
        # main.py.        
        genres_all = pd.Series(df.genres).unique()
        genres_list = []
        for item in genres_all:
            genres_list.append(item.split('|'))
        genres_values = list(set(
                [item for sublist in genres_list for item in sublist])) 
        
        unique_directors = list(set(list(pd.Series(df.director_name).unique())))
        
        # assigning variables to self so they can be accessed and returned
        # by the run function.
        self.processed_data = df_1hot
        self.genres = genres_values
        self.directors = unique_directors
    
    # send it!
    def _run(self):
        self._preprocess()
        return (self.processed_data, self.genres, self.directors)