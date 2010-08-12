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

def geni_update_sol(sol,route,tour,vertex):
    sol[tour]['route']=route;
    if vertex in sol[tour]['inserted']:
        sol[tour]['inserted'][vertex]+=1;
    else:
        sol[tour]['inserted'][vertex]=1;
        
    if vertex in sol[tour]['deleted']:
        sol[tour]['new_tabu']=True;
    
    cost=compute_cost(sol);
    return sol,cost;

def geni_route_type_I(route,node,pos_vi,pos_vj,pos_vk,viplus,vjplus,vkplus,l):
    return route[0:pos_vi]+[node]+geni_reverse(route,pos_vj,viplus)+geni_reverse(route,pos_vk,vjplus)+route[vkplus:l];

def geni_route_type_I_inverse(route,node,pos_vi,pos_vj,pos_vk,viplus,vjplus,vkplus,l):
    route=geni_route_type_I(route,node,pos_vi,pos_vj,pos_vk,viplus,vjplus,vkplus,l);
    route.reverse();
    return route;

def geni_route_type_II(route,node,pos_vi,pos_vj,pos_vk,pos_vl,viplus,vjplus,vkplus,vlplus,l):
    return route[0:pos_vi+1]+[node]+geni_reverse(route,pos_vj,vlplus)+route[vjplus:pos_vk+1]+geni_reverse(route,pos_vl,viplus)+route[vkplus:l];
    
def geni_route_type_II_inverse(route,node,pos_vi,pos_vj,pos_vk,pos_vl,viplus,vjplus,vkplus,vlplus,l):
    route=geni_route_type_II(route,node,pos_vi,pos_vj,pos_vk,pos_vl,viplus,vjplus,vkplus,vlplus,l);
    route.reverse();
    return route;

def geni_type_II_body(node,neighbors,solution,tour,vi,pos_vi,vj,pos_vj,func_2):
    sol=None;
    cost=None;
    if pos_vi>pos_vj:
        vi,pos_vi,vj,pos_vj=geni_swap(vi,pos_vi,vj,pos_vj);
        
    route=solution[tour]['route'];
    l=len(route);
    vjplus_=solution[tour]['route'][(pos_vj+1)%l];
    
    
    
    for vk,pos_vk in neighbors[vjplus_][tour]:
        #print(neighbors);
        #print(vjplus_);
        #print(tour);
        #print(vk);
        for vl,pos_vl in neighbors[vjplus_][tour]:
            #print(vl);
            if pos_vj>pos_vk:
                vj,pos_vj,vk,pos_vk=geni_swap(vj,pos_vj,vk,pos_vk);
            if pos_vl>pos_vj:
                vl,pos_vl,vj,pos_vj=geni_swap(vl,pos_vl,vj,pos_vj);
            if pos_vi>pos_vl:
                vi,pos_vi,vl,pos_vl=geni_swap(vi,pos_vi,vl,pos_vl);
                
            vjplus=(pos_vj+1)%l;
            viplus=(pos_vi+1)%l;
            vkplus=(pos_vk+1)%l;
            vlplus=(pos_vl+1)%l;            
            if pos_vk!=pos_vj and pos_vk!=vjplus and pos_vl!=pos_vi and pos_vl!=viplus:
                
                sol=deepcopy(solution);
                route=func_2(route,node,pos_vi,pos_vj,pos_vk,pos_vl,viplus,vjplus,vkplus,vlplus,l);
                sol,cost=geni_update_sol(sol,route,tour,node);
                #sol[tour]['route']=route;
                #sol[tour]['inserted']=vertex
                #cost=compute_cost(sol);
                
    return sol,cost;

def geni_type_I_body(node,neighbors,solution,tour,vi,pos_vi,vj,pos_vj,func_2):
    sol=None;
    cost=None;
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
            route=func_2(route, node, pos_vi, pos_vj, pos_vk, viplus, vjplus, vkplus,l);
            sol,cost=geni_update_sol(sol,route,tour,node);
            #sol[tour]['route']=route;
            #cost=compute_cost(sol);
            
    return sol,cost;

def geni_main(node,neighbors,solution,func,func_2):
    best_sol=best_cost=cost=sol=None;
    #print(neighbors);
    for tour in neighbors[node].keys():
        for vi,pos_vi in neighbors[node][tour]:
            #print(vi);
            #print(pos_vi);
            for vj,pos_vj in neighbors[node][tour]:
                if vi!=vj:
                    sol,cost=func(node,neighbors,solution,tour,vi,pos_vi,vj,pos_vj,func_2);
                    if (best_cost==None):
                        best_cost=cost;
                        best_sol=sol;
                    elif (cost!=None and (cost[1]<best_cost[1])):
                        best_cost=cost;
                        best_sol=sol;
                            
    return best_sol,best_cost;
    
def geni_type_I(node,neighbors,solution):
    return geni_main(node,neighbors,solution,geni_type_I_body,geni_route_type_I);

def geni_type_II(node,neighbors,solution):
    return geni_main(node,neighbors,solution,geni_type_II_body,geni_route_type_II);

def geni_type_I_inverted(node,neighbors,solution):
    return geni_main(node,neighbors,solution,geni_type_I_body,geni_route_type_I_inverse);

def geni_type_II_inverted(node,neighbors,solution):
    return geni_main(node,neighbors,solution,geni_type_II_body,geni_route_type_II_inverse);

def geni_insert(node,neighbors,solution):
    
    best_sol=best_cost=None;
    first_iteration=True;
    
    for insertion in [geni_type_I,geni_type_I_inverted,
                      geni_type_II,geni_type_II_inverted
                      ]:
        sol,cost=insertion(node,neighbors,solution);
        if(best_cost==None) or (cost!=None and (cost[1]<best_cost[1])):
            best_cost=cost;
            best_sol=sol;
            first_iteration=False;
        
    return best_sol,best_cost;
    
def us(tmp_solution):
    pass;