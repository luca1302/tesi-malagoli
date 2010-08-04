# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 18.33.45$"

def link(node1,node2):
    pass;

def unlink(node1,node2):
    pass;

def delete_from_his_route(node):
    succ=node['succ'];
    prec=node['prec'];

    unlink(node,succ);
    unlink(node,prec);
    link(succ,prec);

def add_as_successor_of(src,successor):
    succ=src['succ'];
    link(src,successor);
    link(successor,succ);

def or1(solution,vertexes,vertex_neighbors):
    delete_from_his_route(neighbor);
    add_as_successor_of(vertex,neighbor);
    

def or2(vertexes,vertex_neighbors):
    pass;
    

def swap(solution):
    pass;
def ab(solution):
    pass;

def make1step(solution):
    solution_set={};
    for move in moves:

        for vertex in vertexes:
            for route,position in vertex_neighbors[vertex]:
                current_solution=copy.deepcopy(solution);
                neighbor=current_solution[route,position];
                tabu=move(vertex,neighbor);
                cost=compute_cost(current_solution);
                if(cost in solution_set):
                    solution_set[cost].append({'route':current_solution,'tabu':tabu});
                else:
                    solution_set[cost]=[{'route':current_solution,'tabu':tabu}];
    return solution_set;
moves=[or1];
