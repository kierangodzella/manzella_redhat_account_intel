README

This repository contains the python files for Account Intelligence project
that I was given by RedHat. The three modules are main, preprocessing, and extra_credit.

The module main.py uses arguments (data, metric, EC) in its execution of principle class 
RunReport. Data is set to the movie_metadata.csv file in the repository, and should not 
be modified. 'metric' can take two different values of 'net' or 'ROI', and is set to 'net' 
by default. This outputs the top ten most profitable genres and directors as measured by 
net revenue; switching 'metric' to "ROI" returns the top genres and directors as measured 
by net revenue as a percentage of budget. 

'EC' is a boolean argument to enable/disable the extra-credit option, which gives the top-ten
actor-director pairs, measured by average IMDb score, and is set True by default. Setting 
'EC' to False will greatly improve runtime, but you'll miss out on some fun facts.

The flow of this project is as follows: main.py imports the two local modules, and runs 
the function "do_all" in its class instance RunReport(data), where (data) is the local csv.
In "do_all", the data is processed by the module proprocessing, and returned to self as the
processed dataframe, a list of all unique genres, and a list of all unique directors.

After preprocessing is completed, "do_all" runs "_ranking". This calculates the average ROI
and net revenue for each genre and director.

If extra credit is enabled, "do_all" uses the module extra_credit to calculate the top ten
actor/director pairs (who have worked on at least two films together) as measured by their 
average IMDb score. 

Finally, "do_all" runs "_output" to print out the top ten genres and directors ranked by 
whichever metric is chosen in the "RunReport" arguments. If extra credit is enabled, it prints
out the actor/director ranking as well. 


NOTE:
I've missed homework, and I appreciated having some coding work to do. In all seriousness, 
it was a lot of fun and felt good. Thank you for taking your time to look over this.


