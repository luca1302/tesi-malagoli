from dummy import dummy_solution
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$2-ago-2010 21.23.40$"


__gts={
        'cost_factors':{'duration':1,'load':1,'time_window':1},
        'delta':1,
};

__cost_factors={'lenght':1,'duration':1};

def gts(customers,max_routes,cicles,**cost_factors):
    initial_solution=dummy_solution(customers,max_routes);
    
    for cost_factor in globals()['__cost_factors'].keys():
        if(cost_factor in cost_factors):
            globals()['__cost_factors'][cost_factor]=cost_factors[cost_factor];

    new_solution=best_solution=initial_solution;
    best_solution_cost=compute_cost(best_solution);

    k=0;
    while (k<cicles):
        new_solution=__choose_new_best_solution(new_solution);
        new_cost=compute_cost(new_solution);
        if(is_feasible(new_solution) and (new_cost<best_solution_cost)):
            best_solution=new_solution;
            best_solution_cost=new_cost;
            k=0;
        else:
            k+=1;
        __update_cost_factors();

    for route in best_solution:
        new_route=__apply_post_opt(route);
        best_solution.remove(route);
        best_solution.append(new_route);

    return best_solution;
