# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 18.33.45$"

from dima import *;
from copy import *;
from common import *;


__tabu_max=50;

def delete_from_his_route(node,node_pos,solution):
    #print('delete({0},{1})'.format(node,node_pos));
    node_tour=node_pos[0];
    node_index=node_pos[1];

    #print(solution[node_tour]['route']);
    value=solution[node_tour]['route'][node_index];
    solution[node_tour]['route'].remove(node);
    #print(solution[node_tour]['route']);
    assert(value==node);

def add_as_successor_of(node,node_pos,new_node,solution):
    node_tour=node_pos[0];
    node_index=node_pos[1];

    assert(solution[node_tour]['route'][node_index]==node);
    solution[node_tour]['route'][node_index+1:node_index+1]=[new_node];
    assert(solution[node_tour]['route'][node_index+1]==new_node);
    solution[node_tour]['new_tabu'][new_node]=globals()['__tabu_max'];

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
        delete_from_his_route(neighbor,neighbor_pos,solution);
        delete_from_his_route(other_neighbor,(neighbor_tour,neighbor_index+1),solution);
        add_as_successor_of(vertex,vertex_pos,neighbor,solution);
        add_as_successor_of(neighbor,(vertex_pos[0],vertex_pos[1]+1),other_neighbor,solution);
        return False;

def swap(solution):
    pass;
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
moves=[or1];
