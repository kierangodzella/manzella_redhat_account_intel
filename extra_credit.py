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
        keycols = ['director_name','actor_1_name','imdb_score']
        for col in keycols:
            df = df[df[col].notnull()]
        df = df[['director_name','actor_1_name','actor_2_name',
                'actor_3_name','imdb_score']]
        
        pair_indexer = pd.DataFrame(columns=['Pair','Score','n'])
        pair_indexer.set_index('Pair', inplace=True)
        pair_list = []
        
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
        pair_indexer_output = (pair_indexer.sort_values('Score', 
                                ascending=False).query('n > 1')
                                .iloc[0:9,:]
                                )
        self.pair_indexer_output = pair_indexer_output
                            
        
        
    def _run(self):
        self._director_actor_pair()
        return self.pair_indexer_output
  
        