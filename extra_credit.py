# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 11:32:09 2019

@author: kiera
"""

import pandas as pd

class ExtraCredit(object):
    def __init__(self, data):
        self.data = data
    
    def _director_actor_pair(self):
        df = self.data
        
        # we're not interested in rows that don't have at least one actor
        # the director, and an IMDb score. We're not using the preprocessed
        # data from main.py because we care about different values, and don't
        # want to erroneously exclude data for missing values we don't need
        keycols = ['director_name','actor_1_name','imdb_score']
        for col in keycols:
            df = df[df[col].notnull()]
        # select relevant rows from the culled dataframe
        df = df[['director_name','actor_1_name','actor_2_name',
                'actor_3_name','imdb_score']]
        
        # intialize an empty dataframe, using the variable "pair" as index,
        # and an empty list for checking repeat pairs
        pair_indexer = pd.DataFrame(columns=['Pair','Score','n'])
        pair_indexer.set_index('Pair', inplace=True)
        pair_list = []
        
        # join is the joined string of director + actor. if that pair has not
        # been seen before, this function adds it to the list and creates a new
        # entry in the pair dataframe. If it has been seen before, it updates
        # the row in the dataframe with a new average score (take current 
        # average score times the number of times it's appeared, plus the new
        # score, divided by n+1) and increments n
        def update(join, pair_indexer):
            if join not in pair_list:
                pair_list.append(join)
                new_entry = pd.DataFrame({'Pair':[join],'Score':
                    [row.imdb_score], 'n': [1]})
                new_entry.set_index('Pair', inplace=True)
                pair_indexer = pair_indexer.append(new_entry)
            elif join in pair_list:
                score = pair_indexer.loc[join,'Score']
                n = pair_indexer.loc[join,'n']
                pair_indexer.loc[join,'Score'] = (score*n 
                                + row.imdb_score)/(n+1)
                pair_indexer.loc[join,'n'] += 1
            return pair_indexer
        
        # this iterator goes row by row, taking at least the top-billed actor
        # and joining the director name with it, then runs the update function
        # above on that combination. We know that each row has at least one
        # actor, and we check to see if there are actors 2, 3 before doing the
        # same with them.
        for i in range(0,df.shape[0]):
            row = df.iloc[i,:]                    
            join = str(row.director_name) + '|' + str(row.actor_1_name)
            pair_indexer = update(join,pair_indexer)
            if row.actor_2_name:
                join = str(row.director_name) + '|' + str(row.actor_2_name)
                pair_indexer = update(join,pair_indexer)
            if row.actor_3_name:
                join = str(row.director_name) + '|' + str(row.actor_3_name)
                pair_indexer = update(join,pair_indexer)
                
        # this wouldn't be very interesting without selecting pairs of actors
        # and directors that have worked on more than one film; otherwise we
        # just get a list of the actor/director pairs composing the top-
        # scoring films in the database. There's room to improve this by 
        # weighing scores of the pairs by the count of films in their score,
        # but this simple implementation is fine to start with.
        pair_indexer_output = (pair_indexer.sort_values('Score', 
                                ascending=False).query('n > 1')
                                .iloc[0:9,:]
                                )
        self.pair_indexer_output = pair_indexer_output
        
    # run output, as called by main.py                        
    def _run(self):
        self._director_actor_pair()
        return self.pair_indexer_output
  
        