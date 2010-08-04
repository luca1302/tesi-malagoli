from trucks import *
from customer import *
from dima import *
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 16.32.33$"

__solution_cost={
    'costs':{'duration':0,'load':1,'time_window':1},
    'cost_factors':{'duration':1,'load':1,'time_window':1},
    'last_solution_feasible':{'duration':True,'load':True,'time_window':True}
};

def compute_cost(solution):
    delta_max_duration=0
    delta_max_load=0;
    delta_time_window=0;

    for customer,attrlist in solution:
        delta_max_duration+=attrlist.delta_distance;
        delta_max_load+=attrlist.delta_load;
        delta_time_window+=attrlist.delta_time_window;
    #for tour in solution:
    #    truck=tour['truck'];
    #    route=tour['route'];
    #    for k in range(len(route)-1):
    #        delta_max_load+=customers[route[k]].demand;
    #        delta_max_duration+=elma[route[k]][route[k+1]];
    #        #delta_time_window+=abs(min(0,service_start_time-opening)+min(0,ending-service_end_time));
    #    delta_max_duration+=elma[route[-1]][route[0]];
    #
    #    delta_max_duration=abs(min(0,truck.time_frame-delta_max_duration));
    #    delta_max_load=abs(min(0,truck.max_load-delta_max_load));

    globals()['__solution_cost']['costs']['load']=delta_max_load;
    globals()['__solution_cost']['costs']['duration']=delta_max_duration;
    globals()['__solution_cost']['costs']['time_window']=delta_time_window;

    alpha=globals()['__solution_cost']['cost_factors']['load'];
    beta=globals()['__solution_cost']['cost_factors']['duration'];
    gamma=globals()['__solution_cost']['cost_factors']['time_window'];

    return delta_max_load*alpha+delta_max_duration*beta+delta_time_window*gamma;

def is_feasible():
    dl=globals()['__solution_cost']['costs']['load'];
    dd=globals()['__solution_cost']['costs']['duration'];
    dt=globals()['__solution_cost']['costs']['time_window'];
    return ((dl==0) and (dd==0) and (dt==0));

def update_cost_factors(delta):
    for key in ['load','distance','time_window']:
        if(globals()['__solution_cost']['costs'][key]!=0):
            ['__solution_cost']['cost_factors']*=(1+delta);
        else:
            ['__solution_cost']['cost_factors']/=(1-delta);
