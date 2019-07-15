# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 20:00:22 2019

@author: kiera
"""
#__name__ == '__main__.'

import pandas as pd

#custom imports

from preprocessing import PreProcessing
from extra_credit import ExtraCredit

class RunReport(object):
    # define init on class instance variables of data, metric, and EC. 
    # data: csv data to be read in
    # metric: 'net' or 'ROI' to select profitability measure
    # EC: boolean; enable/disable execution of extra credit module
    def __init__(self, data, metric, EC=False):
        self.data = data
        self.metric = metric
        self.EC = EC
    
    # do_all is the runfile function, it preprocesses the data, runs the
    # _ranking function on the processed data, runs extra credit if enabled,
    # and runs _output to print to the console    
    def do_all(self):
        self._preprocess()
        self._ranking(self.processed_data, self.genres, self.directors)    
        if self.EC: self._extra_credit(self.data)
        self._output(self.genre_ranker, self.director_ranker, self.metric)
        
    # this just runs the local preprocessing module on the input data
    def _preprocess(self):
        df = self.data
        self.processed_data,self.genres,self.directors = PreProcessing(df)._run()
    
    
    def _ranking(self, processed_data, genres, directors):
        df = processed_data
        
        # intialize empty lists to store results
        genre_performance=[]
        director_performance=[]
        
        for item in genres:
            # iterating through the genres, selecting rows from the input
            # database that are a member of the genre, and then calculating
            # the mean ROI and net for members of that set, then appending
            # those numbers to the list with the genre name.
            selection = df[df[item]==1]
            ROI_average = selection.ROI.sum() / selection.shape[0]
            net_average = selection.net.sum() / selection.shape[0]
            genre_performance.append([item, ROI_average, net_average])
        for item in directors:
            # same thing as above, with directors. The main difference is
            # that directors aren't one-hot encoded
            selection = df[df['director_name']==item]
            ROI_average = selection.ROI.sum() / selection.shape[0]
            net_average = selection.net.sum() / selection.shape[0]
            director_performance.append([item, ROI_average, net_average])
        # assigning class variables to the output dataframes so that 
        # they can be referenced in other functions
        self.genre_ranker = pd.DataFrame(genre_performance, 
                                         columns=['Genre:','ROI','net'])       
        self.director_ranker = pd.DataFrame(director_performance, 
                                            columns=['Director:','ROI','net'])

    def _extra_credit(self, data):
        # optional extra credit module. The option I selected was to output
        # the top-performing actor/director pairs by their average IMDb score
        self.ec_df = ExtraCredit(data)._run()
        
    def _output(self, genre_ranker, director_ranker, metric):
        # customize output based on metric value
        if (metric =='ROI'):
            metric_str = 'return on investment (ROI)'
        elif (metric =='net'):
            metric_str = 'net profit in dollars (gross revenue - budget)'
            # format revenue output to dollar amounts
            pd.options.display.float_format = '${:,.2f}'.format
        else: raise ValueError()
        
        # two-step selection and manipulation, sorting the dataframes by 
        # selected metric in descending order, selecting the first ten,
        # and rounding those values; then selecting the two relevant columns
        # and converting them to a string.
        genre_out = genre_ranker.sort_values(metric, 
                                ascending=False).iloc[0:9,:].round(3)
        genre_out = genre_out[['Genre:',metric]].to_string(index=False)
        
        # same thing as above. After running the output, reset pandas 
        # formatting to default
        director_out = director_ranker.sort_values(metric,
                                ascending=False).iloc[0:9,:].round(3)
        director_out = director_out[['Director:', metric]].to_string(index=False)
        pd.reset_option('display.float_format')
        
        # print out all the custom outputs and the relevant values and tables
        print('The top ten genres on IMDb\'s database, by their mean '
              + metric_str +', are: \n \n', genre_out, '\n')
        print('The top ten directors on IMDb\'s database, by their mean '
              + metric_str +', are: \n \n', director_out,'\n')
        if self.EC:
            print('The top ten director & actor pairs (who have worked on at'+
              ' least two films together) on IMDb\'s database, '+
              'by the mean IMDb scores of their films, are: \n', self.ec_df)

# run if main; autoexecute
if __name__=='__main__':
    input_data = pd.DataFrame(pd.read_csv('movie_metadata.csv'))
    RunReport(data=input_data, metric='net', EC=True).do_all()