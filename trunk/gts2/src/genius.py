# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 18.33.45$"

from copy import *

def geni_swap(x,y):
    return y,x;

def geni_type_I_body(node,neighbors,solution,tour,vi,pos_vi,vj,pos_vj):
    if pos_vi>pos_vj:
        pos_vi,pos_vj=geni_swap(pos_vi,pos_vj);
        #x=pos_vi;
        #pos_vi=pos_vj;
        #pos_vj=pos_vi;
    route=solution[tour]['route'];
    l=len(route);
    print(vj);
    print(route);
    vjplus=solution[tour]['route'][(pos_vj+1)%l];
    print(vjplus);
    print(neighbors);
    for vk,pos_vk in neighbors[vjplus][tour]:
        if pos_vj>pos_vk:
            pos_vj,pos_vk=geni_swap(pos_vj,pos_vk);
            #x=pos_vj;
            #pos_vj=pos_vk;
            #pos_vk=pos_vj;
                            
        if vi!=vk and vk!=vj:
            vjplus=(pos_vj+1)%l;
            vkplus=(pos_vk+1)%l;
            sol=deepcopy(solution);
            route=route[0:pos_vi]+[node]+reverse(route,pos_vj,viplus)+reverse(route,pos_vk,vjplus)+route[vkplus:l];
            sol[tour]['route']=route;
            cost=compute_cost(sol);
    return sol,cost;

def geni_main(node,neighbors,solution,func):
    best_sol=best_cost=cost=sol=None;
    #print(neighbors);
    for tour in neighbors[node].keys():
        for vi,pos_vi in neighbors[node][tour]:
            #print(vi);
            #print(pos_vi);
            for vj,pos_vj in neighbors[node][tour]:
                if vi!=vj:
                    sol,cost=func(node,neighbors,solution,tour,vi,pos_vi,vj,pos_vj);
                    if (best_cost==None):
                        best_cost=cost;
                        best_sol=sol;
                    elif (cost<best_cost):
                        best_cost=cost;
                        best_sol=sol;
                            
    return best_sol,best_cost;
    
def geni_type_I(node,neighbors,solution):
    return geni_main(node,neighbors,solution,geni_type_I_body);

def geni_type_II(node,neighbors,solution):
    return geni_main(node,neighbors,solution,geni_type_II_body);

def geni_insert(node,neighbors,solution):
    
    best_sol=best_cost=None;
    first_iteration=True;
    
    for insertion in [geni_type_I,#geni_type_I_inverted,
                      geni_type_II,#__geni_type_II_inverted
                      ]:
        sol,cost=insertion(node,neighbors,solution);
        if(cost<best_cost) or best_cost==None:
            best_cost=cost;
            best_sol=sol;
            first_iteration=False;
        
    return best_sol,best_cost;
    
def us(tmp_solution):
    pass;