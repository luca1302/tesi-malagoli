# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$1-ago-2010 14.16.51$"

from dima import *
from trucks import *
from customer import *

__solution_cost={
    'costr_factors':{'duration':1,'load':1,'time_window':1,'created':100},
};

def __user_defined_criteria(solution):
    return 0;

def is_elapsed_feasible(solution_cost):
    return solution_cost[3]==0;

def is_load_feasible(solution_cost):
    return solution_cost[2]==0;

def is_time_window_feasible(solution_cost):
    return solution_cost[4]==0;

def compute_cost(solution):
    delta_max_duration=0
    delta_max_load=0;
    delta_time_window=0;
    created=0;

    for tour in solution:
        #print(tour);
        truck=tour['truck'];
        route=tour['route'];
        #print(truck);
        #print(route);
        #print(solution);
        if('created' in tour):
            created+=1;
            del tour['created'];
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

        delta_max_duration=abs(min(0,customers[depot].time_frame-delta_max_duration));
        delta_max_load=abs(min(0,truck.max_load-delta_max_load));


    alpha=globals()['__solution_cost']['costr_factors']['load'];
    beta=globals()['__solution_cost']['costr_factors']['duration'];
    gamma=globals()['__solution_cost']['costr_factors']['time_window'];
    omega=globals()['__solution_cost']['costr_factors']['created'];

    cost_feasible=__user_defined_criteria(solution)+path_lenght+created*omega;
    cost_infeasible=cost_feasible+delta_max_load*alpha+delta_max_duration*beta+delta_time_window*gamma;

    #cost+=__penalty(cost,solution);

    return (cost_feasible,cost_infeasible,delta_max_load,delta_max_duration,delta_time_window);