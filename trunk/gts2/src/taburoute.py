# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 16.32.33$"

#from common import *
from clark_and_wright import *
from random import *
from moves import *
from costs import *

def taburoute(customers,trucks_number,cicles):
    seed(a=123456789);
    initial_solution=Clark_and_Wright(dima,elma,customers,allocate_truck,trucks_number,depot).find_starting_solution();
    
    return Search(5*trucks_number,
                  5,
                  5,
                  10,
                  0.015,
                  10,
                  50*len(customers)).find_solution(initial_solution);

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
        
        self.best_solution=None;
        self.best_solution_cost=-1;
        self.us_already_runned=False;
        self.n=len(customers);
        self.delta_max=0;
        self.m=-1;
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
    
    def __consider_single_routes(self,solution_set,v,tmp_solution):
        if(len(tmp_solution)<m):
            for k in range(len(tmp_solution),m): 
                sol=deepcopy(tmp_solution);
                for tour in sol:
                    for position in tour['route']:
                        if v in tour['route']:
                            tour['route'].remove(v);
                sol.append({'truck':peek_truck(k),'route':[v],'new_tabu':{},'inserted':{},'deleted':{},'old_tabu':{},'created':True});
                __add_to_solution_set(solution_set,sol,calculate_cost(sol)[1]);
    
    def __evaluate_moves(v,tmp_solution,tmp_solution_cost):
        solution_set={};
        
        __consider_single_route(solution_set,v_set,tmp_solution);
        for move in moves:
            sol=move(v,neighbors[v]);
            sol_cost=comput_cost(sol);
            if(__is_tabu(sol)):
                #aspiration criterion
                if(__is_feasible(sol_cost) and sol_cost[0]<tmp_solution_cost[0]):
                    __add_to_solution_set(solution_set,sol,sol_cost[0]);
                    
                elif (not __is_feasible(sol_cost) and sol_cost[1]<tmp_solution_cost[1]):
                    __add_to_solution_set(solution_set,sol,sol_cost[0]);
                        
            else:
                if(sol_cost[1]<tmp_solution_cost[1]):
                    __add_to_solution_set(solution_set,sol,sol_cost[1]);
                else:
                    __add_to_solution_set(solution_set,sol,sol_cost[1]+__penalty(sol));
       
        return solution_set;         
    
    def __best(solution_set):
        min_cost=min(soltion_set.keys());
        return shuffle(solution_set[min_cost])[0],min_cost;
    
    def __improve(self,tmp_solution,tmp_solution_cost,new_solution,new_solution_cost):
        if((new_solution_cost[1]>tmp_solution_cost[1])
            and (__is_feasible(tmp_solution_cost))
            and (not self.us_already_runned)):
            pass;
            tmp_solution=us(tmp_solution);
            self.us_already_runned=True;
            return tmp_solution,compute_cost(tmp_solution);
        else:
            self.us_already_runned=False;
            return new_solution,new_solution_cost;
            
    def __update_cost_factors(self,sol):
        k=self.t%self.update_period;
        
        self.recorded_sol[k]=self.sol;
        
        if((k)==0):
            feasible={factor:True for factor in cost_factors['costraint'].keys()};
            for key,solution in self.recorded_sol.items():
                if(not is_elapsed_feasible(solution)):
                    feasible['e']=False;
                if(not is_load_feasible(solution)):
                    feasible['l']=False;
                if(not is_time_window_feasible(solution)):
                    feasible['tw']=False;
                    
            for factor in cost_factors['costraint'].keys():
                if(not feasible[factor]):
                    cost_factors['costraint'][factor]*=2;
                else:
                    cost_factors['costraint'][factor]/=2;
                    
            self.recorded_sol.clear();        
    
    def __update(v,tmp_solution,tmp_solution_cost):
        new_tabu=False;
        
        for tour in tmp_solution:
            if v in tour['new_tabu']:
                new_tabu=True;
                
        if((not self.us_already_runned)
           and (new_tabu)):
            self.tabu[v]=uniform(self.tabu_min,self.tabu_max);
            
        self.t=t+1;
        
        if(tmp_solution_cost[1]<self.best_solution_cost[1]):
            self.best_solution=tmp_solution;
            self.best_solution_cost=tmp_solution_cost;
            #we must continue a little longer 
            self.t=0;
        
        self.delta_max=max(self.delta_cost,abs(self.old_delta_cost-self.new_delta_cost));
        
        self.m=len(self.best_solution);
        
        __update_cost_factors(tmp_solution);
        
    def find_solution(self,start):
        self.t=1;
        self.tabu={};
        self.solution=[];
        self.best_solution=tmp_solution=start;
        self.best_solution_cost=tmp_solution_cost=compute_cost(tmp_solution);
        
        while(self.t<self.max_iterations):
            self.m=len(self.best_solution);
            v_set=__vertex_selection(tmp_solution,0);
            for v in v_set:
                solution_set=__evaluate_moves(v,tmp_solution,tmp_solution_cost);
                new_solution,new_solution_cost=__best(solution_set);
                tmp_solution,tmp_solution_cost=__improve(tmp_solution,tmp_solution_cost,new_solution,new_solution_cost);
                __update(v,tmp_solution,tmp_solution_cost);
            
        return self.best_solution;