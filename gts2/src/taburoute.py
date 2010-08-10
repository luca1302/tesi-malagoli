# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 16.32.33$"

from common import *
from clark_and_wright import *
from random import *
from moves import *

def taburoute(customers,trucks_number,cicles):
    seed(a=123456789);
    initial_solution=Clark_and_Wright(dima,elma,customers,allocate_truck,trucks_number,depot).find_starting_solution();
    
    return Search(5*m,
                  5,
                  5,
                  10,
                  0.015,
                  10,
                  50).find_solution(initial_solution);

class Search():

    def __init__(self,
                 candidates_number,
                 geni_max_neighbors,
                 tabu_min,
                 tabu_max,
                 penalty_scaling,
                 update_period,
                 max_iterations):
        
        self.vertexes=None;
        self.neighbors=None;
        self.candidates_number=candidates_number;
        self.max_nearest_neighbors=None;
        self.geni_max_neighbors=geni_max_neighbors;
        self.tabu_min=tabu_min;
        self.tabu_max=tabu_max,
        self.penalty_scaling=penalty_scaling;
        self.update_period=update_period;
        self.max_iterations=max_iterations;
        self.t=1;
        self.tabu={};
        self.solution=[];
        
    def __vertex_selection(self,sol,granular_distance):
        vertexes={};
        for t in range(len(sol)):
            tour=sol[t];
            for k in range(len(tour['route'])):
                vertexes[tour['route'][k]]=[t,k];
        self.vertexes=vertexes;
        tmp_vertexes=sample(vertexes,max_candidates);
        
        neighbors={};
        for vertex in tmp_vertexes:
            ne={};
            for element in range(1,len(dima[vertex])):
                distance=dima[vertex][element];
                if distance<granular_distance and element!=vertex:
                    ne[element]=vertexes[element];
            neighbors[vertex]=ne;
            
        self.vertexes=vertexes;
        self.neighbors=neighbors;
        self.best_solution_cost=0;
        
        return tmp_vertexes; 
    
    def __evaluate_moves(v_set,tmp_solution):
        solution_set={};
        
        __consider_single_routes(solution_set,tmp_solution,tmp_solution_cost,tmp_solution_infeasible_cost);
        for v in v_set:
            for move in moves:
                sol=move(v,neighbors[v]);
                sol_cost=comput_cost(sol);
                if(__is_tabu(sol)):
                    #aspiration criterion
                    if(__is_feasible(sol) and sol_cost[0]<tmp_solution_cost):
                        __add_to_solution_set(solution_set,sol,sol_cost[0]);
                    
                    elif (not __is_feasible(sol) and sol_cost[1]<tmp_solution_infeasible_cost):
                        __add_to_solution_set(solution_set,sol,sol_cost[0]);
                        
                else:
                    if(sol_cost[1]<tmp_solution_infeasible_cost):
                        __add_to_solution_set(solution_set,sol,sol_cost[1]);
                    else:
                        __add_to_solution_set(solution_set,sol,sol_cost[1]+__penalty(sol));
       
        return solution_set;         
    
    def __best(solution_set):
        pass;
    
    def find_solution(self,start):
        self.t=1;
        self.tabu={};
        self.solution=[];
        tmp_solution=start;
        self.best_solution_cost=tmp_solution_cost=compute_cost(tmp_solution);
        
        while(self.t<self.max_iterations):
            v_set=__vertex_selection(tmp_solution,0);
            solution_set=__evaluate_moves(v_set,tmp_solutiontmp_solution_cost);
            tmp_solution=__best(solution_set);
            tmp_solution=__improve(tmp_solution);
            __update(tmp_solution);
            
        return self.solution;