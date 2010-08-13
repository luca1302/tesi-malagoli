# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 18.33.45$"

from genius import geni_insert
from copy import *
    
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

def insert(vertex,neighbors,sol):
    #solution[node_tour]['route'][node_index:node_index]=[new_node];
    #assert(solution[node_tour]['route'][node_index]==new_node);
    solution,cost=geni_insert(vertex,neighbors,sol);
    #solution[node_tour]['new_tabu'][new_node]=globals()['__tabu_max'];
    #if(new_node in solution[node_tour]['inserted']):
    #    solution[node_tour]['inserted'][new_node]+=1;
    #    solution[node_tour]['new_tabu'][new_node]=True;
    #else:
    #    solution[node_tour]['inserted'][new_node]=1;
    #    if new_node in solution[node_tour]['deleted']:
    #       solution[node_tour]['new_tabu'][new_node]=True;
    #return solution,cost;
    

def add_as_successor_of(node,node_pos,neighbors,solution):
    node_tour=node_pos[0];
    node_index=node_pos[1];

    assert(solution[node_tour]['route'][node_index]==node);
    return insert_in_position(node,neighbors, node_tour, node_index+1, solution);
    #solution[node_tour]['route'][node_index+1:node_index+1]=[new_node];
    #assert(solution[node_tour]['route'][node_index+1]==new_node);
    #solution[node_tour]['new_tabu'][new_node]=globals()['__tabu_max'];

def or1(vertex,vertex_pos,neighbors,solution):
    #print('or1({0},{1},{2},{3})'.format(vertex,vertex_pos,neighbor,neighbor_pos));
    #sols={};
    sol=deepcopy(solution);
    delete_from_his_route(vertex,vertex_pos,sol);
    #n={tour:neighbor_pos for tour,neighbor_pos in neighbors[vertex].items() if (vertex_pos[0]!=tour)};
    
    #sol,cost=geni_insert((vertex,vertex),neighbors,sol);
    return geni_insert((vertex,vertex),vertex_pos[0],neighbors,sol);
    #sols[cost]=sol;
    #        
    #if len(sols.keys())==0:
    #    return None;
    #else:
    #    min_cost=min(sols.keys());
    #    return sols[min_cost];

def or2(vertex,vertex_pos,neighbors,solution):
    l=len(solution[vertex_pos[0]]['route']);
    if(l<=1):
        return None,None;
    #if(vertex_pos[1]==l-1):
    #    return None,None;
    #else:
        #print('or1({0},{1},{2},{3})'.format(vertex,vertex_pos,neighbor,neighbor_pos));
    #sols={};
    sol=deepcopy(solution);
    #print(sol);
    succ_pos=(vertex_pos[0],(vertex_pos[1]+1)%l);
    #print(vertex,vertex_pos[1],l,succ_pos[1],sol[vertex_pos[0]]['route']);
    succ=sol[succ_pos[0]]['route'][succ_pos[1]];
    #print(sol[succ_pos[0]]['route']);
    #print(solution[succ_pos[0]]['route']);
    if(succ_pos[1]>vertex_pos[1]):
        delete_from_his_route(succ,succ_pos,sol);
        delete_from_his_route(vertex,vertex_pos,sol);
    elif(succ_pos[1]<vertex_pos[1]):
        delete_from_his_route(vertex,vertex_pos,sol);
        delete_from_his_route(succ,succ_pos,sol);
    else:
        return None,None;
    #n={tour:neighbor_pos for tour,neighbor_pos in neighbors[vertex].items() if (vertex_pos[0]!=tour)};
    #print(sol[succ_pos[0]]['route']);
    #print(solution[succ_pos[0]]['route']);
    #sol,cost=geni_insert((vertex,succ),neighbors,sol);
    return geni_insert((vertex,succ),vertex_pos[0],neighbors,sol);
    #sols[cost]=sol;
    #        
    #if len(sols.keys())==0:
    #    return None;
    #else:
    #    min_cost=min(sols.keys());
    #    return sols[min_cost];

def swap(vertex,vertex_pos,neighbors,solution):
    #if(vertex_pos[0]==neighbor_pos[0]):
    #    return True;
    #else:
    
        #delete_from_his_route(vertex, vertex_pos, solution);
        #delete_from_his_route(neighbor, neighbor_pos, solution);
        #insert_in_position(vertex, neighbor_pos[0], neighbor_pos[1], solution);
        #insert_in_position(neighbor, vertex_pos[0], vertex_pos[1], solution);
        #return False;
    sols={};
    l=len(solution[vertex_pos[0]]);
    succ_pos=(vertex_pos[0],(vertex_pos[0]+1)%l);
    succ=solution[succ_pos[0]]['route'][succ_pos[1]];
    for tour in neighbors[succ]:
        if tour!=succ_pos[0]:
            for neighbor in neighbors[succ][tour]:
                #print(neighbors[succ]);
                #print(tour);
                #print(neighbor);
                sol=deepcopy(solution);
                delete_from_his_route(succ,succ_pos,sol);
                delete_from_his_route(vertex,vertex_pos,sol);
                geni_insert((vertex,vertex),neighbors,sol);
                sol,cost=geni_insert((neighbor[0],neighbor[0]),neighbors,sol);
                
                if cost!=None:
                    sols[cost]=sol;
    if len(sols.keys())!=0:
        min_cost=min(sols.keys());
        return sols[min_cost],min_cost;
    else:
        return None,None;
    
def ab(solution):
    pass;

moves=[or1,or2];
