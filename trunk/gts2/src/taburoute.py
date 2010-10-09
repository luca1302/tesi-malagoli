# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 16.32.33$"

#from common import *
from clark_and_wright import *
from random import *
from new_moves import *
from dima import *
from trucks import *
import costs
from math import sqrt
from time import time

def taburoute(customers,trucks_number,cicles,**costs):
    seed(a=123456789);
    
    for factor,coefficient in costs.items():
        globals()['solution_cost']['user_factors'][factor]=coefficient;
        
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
        self.old_delta_cost=self.new_delta_cost=self.delta=0;
        self.m=-1;
        self.t=1;
        self.tabu={};
        self.key_vertex=None;
        self.recorded_sol={};
        self.beta=self.beta1=1.25;
        self.beta2=1.75;
        self.beta_period=self.beta_period1=15*self.n;
        self.beta_period2=self.n;
        self.period_switch=False;
        self.saved_period=0;
        self.start_time=0;
        #self.curr_time=0;
        
    def __init_key(self,vertex):
        self.key_vertex=vertex;
        
        
    def __key(self,x):
        #print(self.key_vertex);
        #print(x);
        return dima[self.key_vertex][x[0]];

    def __build(self,sol,granular_distance):
        vertexes={};
        for t in range(len(sol)):
            tour=sol[t];
            for k in range(len(tour['route'])):
                vertexes[tour['route'][k]]=[t,k];
        self.vertexes=vertexes;
        
        neighbors={};
        for vertex in vertexes:
            ne={};
            for element in range(len(dima[vertex])):
                distance=dima[vertex][element];
                if element!=depot and distance<granular_distance and element!=vertex:
                    neighbor=vertexes[element];
                    neighbor_tour=neighbor[0];
                    if neighbor_tour in ne:
                        ne[neighbor_tour]+=[(element,neighbor[1])];
                    else:
                        ne[neighbor_tour]=[(element,neighbor[1])];
            self.__init_key(vertex);
            
            for tour in ne.keys():
                #print(ne[tour]);
                ne[tour]=sorted(ne[tour],key=self.__key)[1:min(len(ne[tour]),self.geni_max_neighbors)];
            neighbors[vertex]=ne;
            
        #self.vertexes=vertexes;
        self.neighbors=neighbors;
        
    def __vertex_selection(self,sol,granular_distance):
        self.__build(sol, granular_distance);
        #vertexes={};
        #for t in range(len(sol)):
        #    tour=sol[t];
        #    for k in range(len(tour['route'])):
        #        vertexes[tour['route'][k]]=[t,k];
        #self.vertexes=vertexes;
        tmp_vertexes=sample(list(self.vertexes.keys()),min(self.candidates_number,len(self.vertexes.keys())));
        #print(tmp_vertexes);
        #print(self.vertexes.keys());
        #neighbors={};
        #for vertex in vertexes:
        #    ne={};
        #    for element in range(len(dima[vertex])):
        #        distance=dima[vertex][element];
        #        if element!=depot and distance<granular_distance and element!=vertex:
        #            neighbor=vertexes[element];
        #            neighbor_tour=neighbor[0];
        #            if neighbor_tour in ne:
        #                ne[neighbor_tour]+=[(element,neighbor[1])];
        #            else:
        #                ne[neighbor_tour]=[(element,neighbor[1])];
        #    self.__init_key(vertex);
        #    
        #    for tour in ne.keys():
        #        #print(ne[tour]);
        #        ne[tour]=sorted(ne[tour],key=self.__key)[1:min(len(ne[tour]),self.geni_max_neighbors)];
        #    neighbors[vertex]=ne;
            
        #self.vertexes=vertexes;
        #self.neighbors=neighbors;
        #self.best_solution_cost=0;
        
        #return {v:self.vertexes[v] for v in tmp_vertexes};
	return dict((v,self.vertexes[v]) for v in tmp_vertexes); 
    
    def __add_to_solution_set(self,sol_set,sol,cost):
        #print()
        if cost in sol_set:
            sol_set[cost].append(sol);
        else:
            sol_set[cost]=[sol];
    
    def __consider_single_route(self,solution_set,v,tmp_solution):
        if(len(tmp_solution)<self.m):
            for k in range(len(tmp_solution),self.m): 
                sol=deepcopy(tmp_solution);
                for tour in sol:
                    for position in tour['route']:
                        if v in tour['route']:
                            tour['route'].remove(v);
                sol.append({'truck':peek_truck(k),'route':[v],'new_tabu':{},'inserted':{},'deleted':{},'old_tabu':{},'created':True});
                __add_to_solution_set(solution_set,sol,calculate_cost(sol)[1]);
    
    def __is_tabu(self,sol):
        for tour in sol:
            for tabu in self.tabu:
                if tabu in tour['new_tabu']:
                    return True;
        return False;
    
    def __penalty(self,sol,v):
        moved=0;
        #print(sol);
        for tour in sol:
            for key in ['inserted','deleted']:
                if v in tour[key]:
                    moved+=tour[key][v];
        return self.delta*sqrt(self.m)*self.penalty_scaling*(moved/(self.t+1));
    
    def __is_feasible(self,sol_cost):
        return (costs.is_elapsed_feasible(sol_cost) 
                and costs.is_load_feasible(sol_cost) 
                and costs.is_time_window_feasible(sol_cost));
    
    def __evaluate_moves(self,v,v_pos,tmp_solution,tmp_solution_cost):
        solution_set={};
        sol=deepcopy(tmp_solution);
        self.__consider_single_route(solution_set,v,sol);
        for move in moves:
            sol=deepcopy(tmp_solution);
            #print(move);
            #print(self.neighbors);
            sol,sol_cost=move(v,v_pos,self.neighbors,sol);
            if sol==None:
                continue;
            #sol_cost=costs.compute_cost(sol);
            if(self.__is_tabu(sol)):
                #aspiration criterion
                if(self.__is_feasible(sol_cost) and sol_cost[0]<tmp_solution_cost[0]):
                    self.__add_to_solution_set(solution_set,(sol,sol_cost),sol_cost[0]);
                    
                elif (not self.__is_feasible(sol_cost) and sol_cost[1]<tmp_solution_cost[1]):
                    self.__add_to_solution_set(solution_set,(sol,sol_cost),sol_cost[0]);
                        
            else:
                if(sol_cost[1]<tmp_solution_cost[1]):
                    self.__add_to_solution_set(solution_set,(sol,sol_cost),sol_cost[1]);
                else:
                    self.__add_to_solution_set(solution_set,(sol,sol_cost),sol_cost[1]+self.__penalty(sol,v));
       
        return solution_set;         
    
    def __best(self,solution_set):
        if(len(solution_set.keys())!=0):
            min_cost=min(solution_set.keys());
            #print(min_cost);
            couple=sample(solution_set[min_cost],1)[0];
            return couple[0],couple[1];
        else:
            return None,None;
    
    def __improve(self,tmp_solution,tmp_solution_cost,new_solution,new_solution_cost,tour,gran_dist):
        if(new_solution==None):
            self.us_already_runned=False;
        #    tmp_solution=us(tmp_solution);
            return tmp_solution,tmp_solution_cost;
            
        #print(new_solution_cost[1]>tmp_solution_cost[1],self.__is_feasible(tmp_solution_cost),not self.us_already_runned);
        
        elif(not self.__is_feasible(tmp_solution_cost)
           and self.__is_feasible(new_solution_cost)):
            self.us_already_runned=False;
            #print("wow");
            return new_solution,new_solution_cost;
        
        elif((new_solution_cost[1]>tmp_solution_cost[1])
            and (self.__is_feasible(tmp_solution_cost))
            and (not self.us_already_runned)):
            self.__rebuild(tmp_solution, gran_dist);
            #print("running us");
            #print(tmp_solution_cost);
            tmp_solution_,tmp_solution_cost_=us(tmp_solution,tour,self.neighbors,gran_dist);
            #print(tmp_solution_cost_);
            #print("end us");
            self.us_already_runned=True;
            if(tmp_solution_cost_!=None
               and self.__is_feasible(tmp_solution_cost_) 
               and tmp_solution_cost_[1]<tmp_solution_cost[1]):
                tmp_solution=tmp_solution_;
                tmp_solution_cost=tmp_solution_cost_;
            return tmp_solution,tmp_solution_cost;
        else:
            self.us_already_runned=False;
            return new_solution,new_solution_cost;
            
    def __update_cost_factors(self,sol):
        k=self.t%self.update_period;
        
        self.recorded_sol[k]=sol;
        
        if((k)==0):
            cost_factors=costs.solution_cost['costr_factors'];
            #feasible={factor:True for factor in cost_factors.keys()};
	    feasible=dict((factor,True) for factor in cost_factors.keys());
            for key,solution in self.recorded_sol.items():
                if(not costs.is_elapsed_feasible(solution)):
                    feasible['duration']=False;
                if(not costs.is_load_feasible(solution)):
                    feasible['load']=False;
                if(not costs.is_time_window_feasible(solution)):
                    feasible['time_window']=False;
            
            for factor in cost_factors.keys():
                if factor=='created':
                    continue;
                if(not feasible[factor]):
                    cost_factors[factor]*=2;
                else:
                    cost_factors[factor]/=2;
                    
            self.recorded_sol.clear();        
    
    def __update(self,v,tmp_solution,tmp_solution_cost):
        new_tabu=False;
        
        for tour in tmp_solution:
            if v in tour['new_tabu']:
                new_tabu=True;
                del tour['new_tabu'][v];
                
        if((not self.us_already_runned)
           and (new_tabu)):
            self.tabu[v]=uniform(self.tabu_min,self.tabu_max);
            
        self.t+=1;
        
        if(((tmp_solution_cost[1]<self.best_solution_cost[1])and ( self.__is_feasible(self.best_solution_cost)==self.__is_feasible(tmp_solution_cost)))
           or ((not self.__is_feasible(self.best_solution_cost)) and (self.__is_feasible(tmp_solution_cost)))):
            self.best_solution=tmp_solution;
            self.best_solution_cost=tmp_solution_cost;
            #we must continue a little longer 
            self.t=0;
        
        self.new_delta_cost=self.best_solution_cost[1];
        self.delta=abs(self.old_delta_cost-self.new_delta_cost);
        self.old_delta_cost=self.new_delta_cost;
        
        self.m=len(self.best_solution);
        
        self.__update_cost_factors(tmp_solution_cost);
        
    def __rebuild(self,sol,gran_dist):
        self.__build(sol, gran_dist);
        
    def __granular_distance(self,granular_cost):
        #print(self.n);
        #print(self.m);
        #print(granular_cost);
        if self.period_switch:
            self.saved_period+=1;
            if(self.saved_period%self.beta_period)==0:
                self.period_switch=False;
                self.beta=self.beta1;
                self.beta_period=self.beta_period1;
                
        elif (self.t%self.beta_period)==0:
            self.period_switch=True;
            self.beta_period=self.beta_period2;
            self.saved_period=0;
            self.beta=self.beta2;
        
        return self.beta*granular_cost/(self.n+self.m);
    
    def find_solution(self,start):
        self.t=1;
        self.start_time=time();
        self.tabu={};
        self.solution=[];
        self.best_solution=tmp_solution=start;
        granular_cost=self.best_solution_cost=tmp_solution_cost=costs.compute_cost(tmp_solution);
        #print(self.best_solution_cost);
        #return;
        time_limit=480;

        while((self.t<self.max_iterations)
              and ((time()-self.start_time)<=time_limit)):
            self.m=len(self.best_solution);
            granular_distance=self.__granular_distance(granular_cost[1]);
            v_set=self.__vertex_selection(tmp_solution,granular_distance);
            for v in v_set.keys():
                for tabu in self.tabu:
                    self.tabu[tabu]-=1;
                    if self.tabu[tabu]<=0:
                        del self.tabu[tabu];
                v_pos=self.vertexes[v];
                solution_set=self.__evaluate_moves(v,v_pos,tmp_solution,tmp_solution_cost);
                new_solution,new_solution_cost=self.__best(solution_set);
                tmp_solution,tmp_solution_cost=self.__improve(tmp_solution,tmp_solution_cost,new_solution,new_solution_cost,v_pos[0],granular_distance);
                self.__update(v,tmp_solution,tmp_solution_cost);
                self.__rebuild(tmp_solution,granular_distance);
                #print(self.best_solution_cost,tmp_solution_cost);
                #print(self.start_time,time(),time()-self.start_time);
                #print(self.t,self.max_iterations);
                if(time()-self.start_time)>=time_limit:
                    break;
                
        return self.best_solution,self.best_solution_cost;
