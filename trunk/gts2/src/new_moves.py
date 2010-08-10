# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 18.33.45$"

from genius import geni_insert
    
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
    #solution[node_tour]['route'][node_index:node_index]=[new_node];
    #assert(solution[node_tour]['route'][node_index]==new_node);
    geni_insert(new_node,node_tour,node_index,solution);
    #solution[node_tour]['new_tabu'][new_node]=globals()['__tabu_max'];
    if(new_node in solution[node_tour]['inserted']):
        solution[node_tour]['inserted'][new_node]+=1;
        solution[node_tour]['new_tabu'][new_node]=True;
    else:
        solution[node_tour]['inserted'][new_node]=1;
        if new_node in solution[node_tour]['deleted']:
           solution[node_tour]['new_tabu'][new_node]=True; 

def add_as_successor_of(node,node_pos,new_node,solution):
    node_tour=node_pos[0];
    node_index=node_pos[1];

    assert(solution[node_tour]['route'][node_index]==node);
    insert_in_position(new_node, node_tour, node_index+1, solution);
    #solution[node_tour]['route'][node_index+1:node_index+1]=[new_node];
    #assert(solution[node_tour]['route'][node_index+1]==new_node);
    #solution[node_tour]['new_tabu'][new_node]=globals()['__tabu_max'];

def or1(vertex,vertex_pos,neighbors,solution):
    #print('or1({0},{1},{2},{3})'.format(vertex,vertex_pos,neighbor,neighbor_pos));
    solutions={};
    sol=deepcopy(solution);
    delete_from_his_route(neighbor,neighbor_pos,sol);
    for neighbor,neighbor_pos in neighbors:
        if(vertex_pos[0]!=neighbor_pos[0]):
            sol_2=deepcopy(sol);
            add_as_successor_of(vertex,vertex_pos,neighbor,sol_2);
            cost=compute_cost(sol_2);
            sols[cost]=sol_2;
            
    if len(sols.keys())==0:
        return None;
    else:
        min_cost=min(sols.keys());
        return sols[min_cost];

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

moves=[or1,or2,swap];
