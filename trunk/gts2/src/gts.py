from common import *
#from dummy import dummy_solution
from clark_and_wright import *
from random import shuffle
from moves import *
#import sys;
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$2-ago-2010 21.23.40$"



__gts={
        'delta':0.5,
        'cost_factor_max_value':6400,
        'cost_factor_min_value':1,
        'update_delay':10
};

__cost_factors={'lenght':1,'duration':1};

def __argmin(solution_set,best_solution_cost):
    min_cost=min(solution_set.keys());
    argmin=None;
    
    #aspiration_criterion
    if(min_cost>=best_solution_cost):
        cost_tmp=None;
        solution_tmp=None;
        
        for cost in sorted(solution_set.keys()):
            #print('cost={0},min_cost={1}'.format(cost,min_cost));
            cost_tmp=cost;
            k=0;
            for solution in solution_set[cost]:
                solution_tmp=k;
                k+=1;
                acceptable=True;
                for tour in solution:
                    for key in tour['new_tabu']:
                        if(key in tour['old_tabu']):
                            acceptable=False;
                    if(not acceptable):
                        break;
                if(acceptable):
                    break;
            if(acceptable):
                break;
            
        argmin=solution_set[cost_tmp][solution_tmp];

    else:
        shuffle(solution_set[min_cost]);
        argmin=solution_set[min_cost][0];
    
    #for tour in argmin:
    #    for key in tour['new_tabu'].keys():
    #        if(key in tour['old_tabu']):
    #            tour['old_tabu']=tour['new_tabu'];
    #tour['new_tabu']={};
        
    return argmin;

def __choose_new_best_solution(solution,best_solution_cost):
    solution_set=make1step(solution);
    solution=__argmin(solution_set,best_solution_cost);
    apply(solution);
    return solution;

def gts(customers,max_routes,cicles,**cost_factors):
    #initial_solution=dummy_solution(customers,max_routes);
    initial_solution=Clark_and_Wright(dima,elma,customers,allocate_truck,trucks_number,depot).find_starting_solution();
    print(initial_solution);
    #sys.exit();
    for cost_factor in globals()['__cost_factors'].keys():
        if(cost_factor in cost_factors):
            globals()['__cost_factors'][cost_factor]=cost_factors[cost_factor];

    new_solution=best_solution=initial_solution;
    best_solution_cost=compute_cost(best_solution);
    print(best_solution);
    print(best_solution_cost);
    update=update_max=globals()['__gts']['update_delay'];
    k=0;
    init_granular(best_solution_cost);
    while (k<cicles):
        #print('next cicle');
        new_solution=__choose_new_best_solution(new_solution,best_solution_cost);
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
