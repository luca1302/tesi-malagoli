# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 18.33.45$"

from copy import *
from costs import compute_cost

def geni_swap(a,x,b,y):
    return b,y,a,x;

def geni_reverse(l,fin,init):
    #print(fin);
    #print(init);
    q=l[init:fin+1];
    q.reverse();
    return q;

def geni_type_II_body(node,neighbors,solution,tour,vi,pos_vi,vj,pos_vj):
    if pos_vi>pos_vj:
        vi,pos_vi,vj,pos_vj=geni_swap(vi,pos_vi,vj,pos_vj);
        
    route=solution[tour]['route'];
    l=len(route);
    vjplus=solution[tour]['route'][(pos_vj+1)%l];
    
    for vk,pos_vk in neighbors[vjplus][tour]:
        for vl,pos_vl in neighbors[vjplus][tour]:
            if pos_vj>pos_vk:
                vj,pos_vj,vk,pos_vk=geni_swap(vj,pos_vj,vk,pos_vk);
            if pos_vl>pos_vj:
                vl,pos_vl,vj,pos_vj=geni_swap(vl,pos_vl,vj,pos_vj);
                
            vjplus=(pos_vj+1)%l;
            viplus=(pos_vi+1)%l;
            vkplus=(pos_vk+1)%l;
            vlplus=(pos_vl+1)%l;            
            if pos_vk!=pos_vj and pos_vk!=vjplus and pos_vl!=pos_vi and pos_vl!=viplus:
                
                sol=deepcopy(solution);
                route=route[0:pos_vi+1]+[node]+geni_reverse(route,pos_vj,vlplus)+route[vjplus:pos_vk+1]+geni_reverse(route,pos_vl,viplus)+route[vkplus:l];
                sol[tour]['route']=route;
                cost=compute_cost(sol);
    return sol,cost;

def geni_type_I_body(node,neighbors,solution,tour,vi,pos_vi,vj,pos_vj):
    if pos_vi>pos_vj:
        vi,pos_vi,vj,pos_vj=geni_swap(vi,pos_vi,vj,pos_vj);
        
    route=solution[tour]['route'];
    l=len(route);
    vjplus=solution[tour]['route'][(pos_vj+1)%l];
    
    for vk,pos_vk in neighbors[vjplus][tour]:
        if pos_vj>pos_vk:
            vj,pos_vj,vk,pos_vk=geni_swap(vj,pos_vj,vk,pos_vk);
                            
        if vi!=vk and vk!=vj:
            vjplus=(pos_vj+1)%l;
            viplus=(pos_vi+1)%l;
            vkplus=(pos_vk+1)%l;
            sol=deepcopy(solution);
            route=route[0:pos_vi]+[node]+geni_reverse(route,pos_vj,viplus)+geni_reverse(route,pos_vk,vjplus)+route[vkplus:l];
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
                    elif (cost[1]<best_cost[1]):
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
        if(best_cost==None) or (cost[1]<best_cost[1]):
            best_cost=cost;
            best_sol=sol;
            first_iteration=False;
        
    return best_sol,best_cost;
    
def us(tmp_solution):
    pass;