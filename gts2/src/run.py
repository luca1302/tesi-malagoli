# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$1-ago-2010 14.16.51$"

from taburoute import *
from trucks import trucks_number
from customer import customers
from dima import *

import sys

if __name__ == "__main__":
	#print(sys.argv[1],sys.argv[2]);
	sol,cost=taburoute(set(range(len(customers)))-set([0]),trucks_number(),50,lenght=int(sys.argv[1]),elapsed=int(sys.argv[2]));

	path_lenght=0;
	curr_max_duration=0;
	for tour in sol:
		route=tour['route'];
        	if(len(route)==0):
            		continue;
		curr_max_duration+=elma[depot][route[0]];
        	path_lenght+=dima[depot][route[0]];
        	for k in range(len(route)-1):
            		path_lenght+=dima[route[k]][route[k+1]];
            		curr_max_duration+=elma[route[k]][route[k+1]];
            	curr_max_duration+=elma[route[-1]][depot];
        	path_lenght+=dima[route[-1]][depot];
	print sys.argv[1],sys.argv[2],path_lenght,curr_max_duration;
