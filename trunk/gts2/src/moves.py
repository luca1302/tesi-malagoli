# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 18.33.45$"

from dima import *;
from copy import *;
from common import *;
from customer import customers;
from math import log10


__tabu_max=int(7.5*log10(n));


def delete_from_his_route(node,node_pos,solution):
    #print('delete({0},{1})'.format(node,node_pos));
    node_tour=node_pos[0];
    node_index=node_pos[1];

    #print(solution[node_tour]['route']);
    value=solution[node_tour]['route'][node_index];
    solution[node_tour]['route'].remove(node);
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
        delete_from_his_route(other_neighbor,(neighbor_tour,neighbor_index+1),solution);
        delete_from_his_route(neighbor,neighbor_pos,solution);
        
        add_as_successor_of(vertex,vertex_pos,neighbor,solution);
        add_as_successor_of(neighbor,(vertex_pos[0],vertex_pos[1]+1),other_neighbor,solution);
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

def get_vertexes(solution):
    vertexes={};
    for tour in range(len(solution)):
        for position in range(1,len(solution[tour]['route'])):
            vertexes[solution[tour]['route'][position]]=(tour,position);
    return vertexes;

def get_neighbors(vertexes):
    neighbors={};
    for vertex in vertexes:
        n={};
        for element in range(1,len(dima[vertex])):
            distance=dima[vertex][element];
            if distance!=None and element!=vertex:
                #if distance in n:
                #    n[distance].append(vertexes[element]);
                #else:
                #    n[distance]=[vertexes[element]];
                n[element]=vertexes[element];
        neighbors[vertex]=n;
    #print(neighbors);
    return neighbors;

def make1step(solution):
    solution_set={};
    for tour in solution:
        for key in tour['old_tabu'].keys():
            tour['old_tabu']-=1;
            if(tour['old_tabu']==0):
                del tour['old_tabu'];
    
    for move in moves:
        vertexes=get_vertexes(solution);
        vertex_neighbors=get_neighbors(vertexes);
        for vertex in vertexes:
            for neighbor in vertex_neighbors[vertex]:
                #print(vertex_neighbors[vertex]);
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

moves=[or1,or2,swap];
