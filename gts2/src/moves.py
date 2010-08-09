# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 18.33.45$"

from dima import *;
from copy import *;
from common import *;
from customer import customers;
from math import log10
import sys;

__tabu_max=int(7.5*log10(n));

__vertexes=None;
__neighbors=None;

__i=0;
__period_1=15
__period_2=1;
__period=__period_1;
__beta_1=1.25;
__beta_2=1.75;
__beta=__beta_1;
__granular_distance=0;
z=0;

def init_granular(z):
    globals()['z']=z;

def apply(argmin):
    #print(argmin);
    #tmp_vertexes=globals()['__vertexes'];
    #tmp_neighbors=globals()['__neighbors'];
    #print(globals()['__neighbors']);
    #print(globals()['__vertexes']);
    for tour in argmin:
        #print(tour);
        if(len(tour['new_tabu'])!=0 or len(tour['deleted'])!=0):
            #print(tour);
            for key in tour['new_tabu'].keys():
                element_index=tour['route'].index(key);
                tour['old_tabu']=tour['new_tabu'];
                
            route_number=argmin.index(tour);
            for k in range(1,len(tour['route'])):
                element=tour['route'][k];
                #print(element);
                globals()['__vertexes'][element][0]=route_number;
                globals()['__vertexes'][element][1]=k;
            tour['deleted'].clear();
            #assert(globals()['__vertexes'][key][0]!=tmp_vertexes[key][0]);
            #assert(globals()['__vertexes'][key][1]!=tmp_vertexes[key][1]);
            #assert(globals()['__vertexes'] is tmp_vertexes);
            #print(globals()['__vertexes'][key]);
            #print(tmp_vertexes[key]);
            #sys.exit();
        tour['new_tabu'].clear();
    #print(globals()['__vertexes']);
    #print(globals()['__neighbors']);
    

def delete_from_his_route(node,node_pos,solution):
    #print('delete({0},{1})'.format(node,node_pos));
    node_tour=node_pos[0];
    node_index=node_pos[1];
    #print(node_pos);
    #print(node);
    #print(solution[node_tour]['route']);
    value=solution[node_tour]['route'][node_index];
    solution[node_tour]['route'].remove(node);
    solution[node_tour]['deleted'][node]=node_index;
    #print(solution[node_tour]['route']);
    assert(value==node);

def insert_in_position(new_node,node_tour,node_index,solution):
    solution[node_tour]['route'][node_index:node_index]=[new_node];
    assert(solution[node_tour]['route'][node_index]==new_node);
    solution[node_tour]['new_tabu'][new_node]=globals()['__tabu_max'];
    if(new_node in solution[node_tour]['inserted']):
        solution[node_tour]['inserted'][new_node]+=1;
    else:
        solution[node_tour]['inserted'][new_node]=1;

def add_as_successor_of(node,node_pos,new_node,solution):
    node_tour=node_pos[0];
    node_index=node_pos[1];

    assert(solution[node_tour]['route'][node_index]==node);
    insert_in_position(new_node, node_tour, node_index+1, solution);
    #solution[node_tour]['route'][node_index+1:node_index+1]=[new_node];
    #assert(solution[node_tour]['route'][node_index+1]==new_node);
    #solution[node_tour]['new_tabu'][new_node]=globals()['__tabu_max'];

def or1(vertex,vertex_pos,neighbor,neighbor_pos,solution):
    #print('or1({0},{1},{2},{3})'.format(vertex,vertex_pos,neighbor,neighbor_pos));
    if(vertex_pos[0]!=neighbor_pos[0]):
        delete_from_his_route(neighbor,neighbor_pos,solution);
        add_as_successor_of(vertex,vertex_pos,neighbor,solution);
        return False;
    else:
        return True;

def or2(vertex,vertex_pos,neighbor,neighbor_pos,solution):
    neighbor_tour=neighbor_pos[0];
    neighbor_index=neighbor_pos[1];
    neighbor_route_lenght=len(solution[neighbor_tour]['route']);
    if((vertex_pos[0]==neighbor_pos[0]) or (neighbor_index==(neighbor_route_lenght-1))):
        return True;
    else:
        other_neighbor=solution[neighbor_tour]['route'][neighbor_index+1];
        delete_from_his_route(other_neighbor,[neighbor_tour,neighbor_index+1],solution);
        delete_from_his_route(neighbor,neighbor_pos,solution);
        
        add_as_successor_of(vertex,vertex_pos,neighbor,solution);
        add_as_successor_of(neighbor,[vertex_pos[0],vertex_pos[1]+1],other_neighbor,solution);
        return False;

def swap(vertex,vertex_pos,neighbor,neighbor_pos,solution):
    if(vertex_pos[0]==neighbor_pos[0]):
        return True;
    else:
        delete_from_his_route(vertex, vertex_pos, solution);
        delete_from_his_route(neighbor, neighbor_pos, solution);
        insert_in_position(vertex, neighbor_pos[0], neighbor_pos[1], solution);
        insert_in_position(neighbor, vertex_pos[0], vertex_pos[1], solution);
        return False;
    
def ab(solution):
    pass;

def get_vertexes(solution,reinit):
    vertexes=globals()['__vertexes'];
    if((vertexes==None) or reinit):
        vertexes={};
        for tour in range(len(solution)):
            #print(solution[tour]['route']);
            for position in range(len(solution[tour]['route'])):
                #print(solution[tour]['route'][position]);
                vertexes[solution[tour]['route'][position]]=[tour,position];
        globals()['__vertexes']=vertexes;
    
    return vertexes;

def get_neighbors(vertexes,granular_distance,reinit):
    neighbors=globals()['__neighbors'];
    if((neighbors==None) or reinit):
        neighbors={};
        for vertex in vertexes:
            #print(vertex);
            n={};
            for element in range(1,len(dima[vertex])):
                #print(element);
                distance=dima[vertex][element];
                if distance<granular_distance and element!=vertex:
                    #if distance in n:
                    #    n[distance].append(vertexes[element]);
                    #else:
                    #    n[distance]=[vertexes[element]];
                    #print(vertexes);
                    n[element]=vertexes[element];
            neighbors[vertex]=n;
        globals()['__neighbors']=neighbors;
    #print(neighbors);
    return neighbors;

def make1step(solution):
    globals()['__i']=(globals()['__i']+1)%(globals()['__period']);
    #print(globals()['__i']);
    if(globals()['__i']==1):
        reinit=True;
        if(globals()['__period']==globals()['__period_1']):
            globals()['__period']=globals()['__period_2'];
            globals()['__beta']=globals()['__beta_2'];
        else:
            globals()['__period']=globals()['period_1'];
            globals()['__beta']=globals()['__beta_1'];
        globals()['__granular_distance']=globals()['__beta']*globals()['z']/(globals()['n']+globals()['m']);
        #print(globals()['z']);
        #print(globals()['__granular_distance']);
    else:
        reinit=False;
      
        
    for tour in solution:
        for key in tour['old_tabu'].keys():
            tour['old_tabu'][key]-=1;
            if(tour['old_tabu'][key]==0):
                del tour['old_tabu'][key];
    
    solution_set={};
    for move in moves:
        vertexes=get_vertexes(solution,reinit);
        vertex_neighbors=get_neighbors(vertexes,globals()['__granular_distance'],reinit);
        for vertex in vertexes:
            #print(vertex_neighbors[vertex]);
            for neighbor in vertex_neighbors[vertex]:
                #print(vertex);
                #print(neighbor);
                current_solution=deepcopy(solution);
                abort=move(vertex,
                        vertexes[vertex],
                        neighbor,
                        vertex_neighbors[vertex][neighbor],
                        current_solution);
                if(not abort):
                    cost=compute_cost(current_solution);
                    if(cost in solution_set):
                        solution_set[cost].append(current_solution);
                    else:
                        solution_set[cost]=[current_solution];
    return solution_set;

moves=[or2];
