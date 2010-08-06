from customer import *
from dima import *
from trucks import *
from math import sqrt
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 16.32.33$"


n=len(customers);
m=trucks_number();
__penalty_factor=0.015;

__solution_cost={
    'costs':{'duration':1,'load':1,'time_window':1},
    'cost_factors':{'duration':1,'load':1,'time_window':1},
    'last_solution_feasible':{'duration':True,'load':True,'time_window':True}
};

def __penalty(cost,solution):
    sum_inserted=0;
    for tour in solution:
        for value in tour['inserted'].values():
            sum_inserted+=value;
    
    return __penalty_factor*cost*sqrt(n*m)*sum_inserted;

def __user_defined_criteria(path_lenght):
    return path_lenght;

def compute_cost(solution):
    delta_max_duration=0
    delta_max_load=0;
    delta_time_window=0;

    for tour in solution:
        #print(tour);
        truck=tour['truck'];
        route=tour['route'];
        #print(truck);
        #print(route);
        #print(solution);
        truck_arrival=elma[depot][route[0]];
        path_lenght=dima[depot][route[0]];
        for k in range(len(route)-1):
            customer=customers[route[k]];
            truck_start_service=max(truck_arrival,customer.opening);
            truck_departure=truck_start_service+download_time(customer);
            
            delta_max_load+=customer.demand;
            path_lenght+=dima[route[k]][route[k+1]];
            delta_max_duration+=elma[route[k]][route[k+1]];
            delta_time_window+=abs(min(0,truck_departure-customer.closing));
        delta_max_duration+=elma[route[-1]][depot];
        path_lenght+=dima[route[-1]][depot];

        delta_max_duration=abs(min(0,truck.time_frame-delta_max_duration));
        delta_max_load=abs(min(0,truck.max_load-delta_max_load));

    globals()['__solution_cost']['costs']['load']=delta_max_load;
    globals()['__solution_cost']['costs']['duration']=delta_max_duration;
    globals()['__solution_cost']['costs']['time_window']=delta_time_window;

    alpha=globals()['__solution_cost']['cost_factors']['load'];
    beta=globals()['__solution_cost']['cost_factors']['duration'];
    gamma=globals()['__solution_cost']['cost_factors']['time_window'];

    cost=__user_defined_criteria(path_lenght);
    cost+=delta_max_load*alpha+delta_max_duration*beta+delta_time_window*gamma;

    cost+=__penalty(cost,solution);

    return cost;

def is_feasible():
    dl=globals()['__solution_cost']['costs']['load'];
    dd=globals()['__solution_cost']['costs']['duration'];
    dt=globals()['__solution_cost']['costs']['time_window'];
    return ((dl==0) and (dd==0) and (dt==0));

def update_cost_factors(delta):
    for key in globals()['__solution_cost']['cost_factors'].keys():
        if(globals()['__solution_cost']['costs'][key]!=0):
            globals()['__solution_cost']['cost_factors'][key]*=(1+delta);
        else:
            globals()['__solution_cost']['cost_factors'][key]/=(1-delta);
