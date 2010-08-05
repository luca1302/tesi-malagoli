from common import *
from dummy import dummy_solution
from random import shuffle
from moves import *
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$2-ago-2010 21.23.40$"


__gts={
        'delta':0.1,
        'cost_factor_max_value':6400,
        'cost_factor_min_value':1,
        'update_delay':10
};

__cost_factors={'lenght':1,'duration':1};

def __choose_new_best_solution(solution):
    
    solution_set=make1step(solution);
    min_cost=min(solution_set.keys());
    shuffle(solution_set[min_cost]);
    return solution_set[min_cost][0];

def gts(customers,max_routes,cicles,**cost_factors):
    initial_solution=dummy_solution(customers,max_routes);
    print(initial_solution);
    
    for cost_factor in globals()['__cost_factors'].keys():
        if(cost_factor in cost_factors):
            globals()['__cost_factors'][cost_factor]=cost_factors[cost_factor];

    new_solution=best_solution=initial_solution;
    best_solution_cost=compute_cost(best_solution);
    print(best_solution);
    print(best_solution_cost);
    update=update_max=globals()['__gts']['update_delay'];
    k=0;
    while (k<cicles):
        new_solution=__choose_new_best_solution(new_solution);
        print(new_solution);
        new_cost=compute_cost(new_solution);
        print(new_cost);
        if(is_feasible() and (new_cost<best_solution_cost)):
            best_solution=new_solution;
            best_solution_cost=new_cost;
            k=0;
        else:
            k+=1;
        if(update<=0):
            update_cost_factors(globals()['__gts']['delta']);
            update=update_max;
            best_solution_cost=compute_cost(best_solution);
        else:
            update-=1;

    #for route in best_solution:
    #    new_route=__apply_post_opt(route);
    #    best_solution.remove(route);
    #    best_solution.append(new_route);

    return best_solution;
