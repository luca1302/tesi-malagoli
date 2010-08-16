# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 18.33.45$"

from copy import *
from costs import compute_cost
#import sys;

def geni_swap(a,x,b,y):
    return b,y,a,x;

def geni_sorting_key(v):
    return v[1];

def geni_sort(v,p,pos_vi):
    q=[];
    r=[];
    #print(p);
    assert(len(v)==len(p));
    for k in range(len(v)):
        q+=[(v[k],p[k])];
    #print(q);    
    q=sorted(q,key=geni_sorting_key);
    
    for el,p in q:
        r+=[el,p];
        
    return r;
    #q=[];
    #r=deepcopy(p);
    #r=sorted(r);
    #i=r.index(pos_vi);
    #l=len(r);
    #print(v,p,i,l);
    #for k in range(l):
    #    done=False;
    #    for j in range(l):
    #        if(r[(i+k)%l]==p[j]) and(not done):
    #            print(r,i,k,j,p,q,done);
    #            done=True;
    #            q+=[v[(i+k)%l],p[(i+k)%l]];
    #            print(r,i,k,j,p,q,done);
    #return q;        
    
    
    #base=pos_vi;
    #
    #if(pos_vj<base):
    #    pos_j=l+pos_vj;
    #if(pos_vk<base):
    #    pos_k=l+pos_vk;
    #
    #if(pos_vj<base) and(pos_vk>base):
    #    return vk,pos_vk,vj,pos_vj,vi,pos_vi;
    #elif(pos_j>pos_k):
    #    return vi,pos_vi,vk,pos_vk,vj,pos_vj;
    #else:
    #    return vi,pos_vi,vj,pos_vj,vk,pos_vk;

def geni_straight(r,init,fin):
    if(fin==(-1)):
        fin=len(r);
    if(fin<init):
        q=r[init:len(r)]+r[0:fin+1];
    else:
        q=r[init:fin+1];
    #print(init,fin,q);
    return q;

def geni_reverse(l,fin,init):
    #print(fin);
    #print(init);
    #q=l[init:fin+1];
    q=geni_straight(l,init,fin);
    #print(q);
    q.reverse();
    #print(q);
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
    #print('geni_type_I');
    #print(node,pos_vi,pos_vj,pos_vk,viplus,vjplus,vkplus);
    #print(route);
    if(vkplus==pos_vi):
        vkplus=pos_vi-1;
    route=route[pos_vi:pos_vi+1]+list(node)+geni_reverse(route,pos_vj,viplus)+geni_reverse(route,pos_vk,vjplus)+geni_straight(route,vkplus,pos_vi-1);
    
    #print(route);
    assert(len(route)==(l+len(node)));
    return route;

def geni_route_type_I_inverse(route,node,pos_vi,pos_vj,pos_vk,viplus,vjplus,vkplus,l):
    #print(route);
    route=geni_route_type_I(route,node,pos_vi,pos_vj,pos_vk,viplus,vjplus,vkplus,l);
    #print(route);
    route.reverse();
    #print(route);
    return route;

def geni_route_type_II(route,node,pos_vi,pos_vj,pos_vk,pos_vl,viplus,vjplus,vkplus,vlplus,l):
    #print('geni_type_II');
    #print(node,pos_vi,pos_vl,pos_vj,pos_vk,viplus,vlplus,vjplus,vkplus);
    #print(route);
    if(vkplus==pos_vi):
        vkplus=pos_vi-1;
    route=route[pos_vi:pos_vi+1]+list(node)+geni_reverse(route,pos_vj,vlplus)+geni_straight(route,vjplus,pos_vk)+geni_reverse(route,pos_vl,viplus)+geni_straight(route,vkplus,pos_vi-1);
    
    #print(route);
    assert(len(route)==(l+len(node)));
    return route;
    
def geni_route_type_II_inverse(route,node,pos_vi,pos_vj,pos_vk,pos_vl,viplus,vjplus,vkplus,vlplus,l):
    route=geni_route_type_II(route,node,pos_vi,pos_vj,pos_vk,pos_vl,viplus,vjplus,vkplus,vlplus,l);
    route.reverse();
    #print(route);
    return route;

def geni_type_II_body(node,neighbors,solution,tour,vi,pos_vi,vj,pos_vj,func_2):
    sol=cost=best_cost=best_sol=None;
    if pos_vi>pos_vj:
        vi,pos_vi,vj,pos_vj=geni_swap(vi,pos_vi,vj,pos_vj);
        
    route=solution[tour]['route'];
    l=len(route);
    vjplus_=solution[tour]['route'][(pos_vj+1)%l];
    
    
    if(tour not in neighbors[vjplus_]):
        return None,None;
    for vk,pos_vk in neighbors[vjplus_][tour]:
        #print(neighbors);
        #print(vjplus_);
        #print(tour);
        #print(vk);
        for vl,pos_vl in neighbors[vjplus_][tour]:
            #print(vl);
            #pos_vi,pos_vl,pos_vj,pos_vk=sorted((pos_vi,pos_vl,pos_vj,pos_vk));
            vi,pos_vi,vl,pos_vl,vj,pos_vj,vk,pos_vk=geni_sort([vi,vl,vj,vk],[pos_vi,pos_vl,pos_vj,pos_vk],pos_vi);
            #if pos_vj>pos_vk:
            #    vj,pos_vj,vk,pos_vk=geni_swap(vj,pos_vj,vk,pos_vk);
            #if pos_vl>pos_vj:
            #    vl,pos_vl,vj,pos_vj=geni_swap(vl,pos_vl,vj,pos_vj);
            #if pos_vi>pos_vl:
            #    vi,pos_vi,vl,pos_vl=geni_swap(vi,pos_vi,vl,pos_vl);
                
            vjplus=(pos_vj+1)%l;
            viplus=(pos_vi+1)%l;
            vkplus=min((pos_vk+1),l);
            vlplus=(pos_vl+1)%l;            
            if (pos_vi!=pos_vl 
                and pos_vl!=pos_vj 
                and pos_vj!=pos_vk 
                and vl!=vi 
                and pos_vk!=pos_vj 
                and pos_vk!=vjplus 
                and pos_vl!=pos_vi 
                and pos_vl!=viplus):
                #assert(pos_vi<pos_vl<pos_vj<pos_vk);
                sol=deepcopy(solution);
                route=sol[tour]['route'];
                route=func_2(route,node,pos_vi,pos_vj,pos_vk,pos_vl,viplus,vjplus,vkplus,vlplus,l);
                #assert(len(route)==(l+len(node)));
                for i in range(len(route)):
                    for j in range(len(route)):
                        if(i!=j):
                            #print(route);
                            assert(route[i]!=route[j]);
                sol,cost=geni_update_sol(sol,route,tour,node);
                #sol[tour]['route']=route;
                #sol[tour]['inserted']=vertex
                #cost=compute_cost(sol);
                if(best_cost==None) or (cost[1]<best_cost[1]):
                    best_cost=cost;
                    best_sol=sol;
                
    return sol,cost;

def geni_type_I_body(node,neighbors,solution,tour,vi,pos_vi,vj,pos_vj,func_2):
    sol=cost=best_cost=best_sol=None;
    #print("route type I");
    #print(node);
    #print(pos_vi);
    #if pos_vi>pos_vj:
    #    vi,pos_vi,vj,pos_vj=geni_swap(vi,pos_vi,vj,pos_vj);
        
    route=solution[tour]['route'];
    l=len(route);
    vjplus_=solution[tour]['route'][(pos_vj+1)%l];
    if(tour not in neighbors[vjplus_]):
        return None,None;
    
    for vk,pos_vk in neighbors[vjplus_][tour]:
        #if pos_vj>pos_vk:
        #    vj,pos_vj,vk,pos_vk=geni_swap(vj,pos_vj,vk,pos_vk);
        #if pos_vi>pos_vj:
        #    vi,pos_vi,vj,pos_vj=geni_swap(vi, pos_vi, vj, pos_vj);
        #print(route);
        #print(node);
        #print(vi,pos_vi,vj,pos_vj,vk,pos_vk);
        vi_,pos_vi_,vj_,pos_vj_,vk_,pos_vk_=geni_sort([vi,vj,vk],[pos_vi,pos_vj,pos_vk],pos_vi);
        #print(vi_,pos_vi_,vj_,pos_vj_,vk_,pos_vk_);                    
        if vi_!=vk_ and vk_!=vj_ and vi_!=vj_:
            assert(pos_vi_!=pos_vj_!=pos_vk_);
            vjplus=(pos_vj_+1)%l;
            viplus=(pos_vi_+1)%l;
            vkplus=min((pos_vk_+1),l);
            sol=deepcopy(solution);
            route=sol[tour]['route'];
            #print(route);
            route=func_2(route, node, pos_vi_, pos_vj_, pos_vk_, viplus, vjplus, vkplus,l);
            
            for i in range(len(route)):
                    for j in range(len(route)):
                        if(i!=j):
                            #print(route);
                            assert(route[i]!=route[j]);
            sol,cost=geni_update_sol(sol,route,tour,node);
            #print(cost);
            if(best_cost==None) or (cost[1]<best_cost[1]):
                best_cost=cost;
                best_sol=sol;
            #sol[tour]['route']=route;
            #cost=compute_cost(sol);
            
    return best_sol,best_cost;


def geni_route(node,vi,pos_vi,tour,neighbors,solution,func,func_2):
    best_sol=best_cost=cost=sol=None;
    #print(vi,pos_vi);
    for vj,pos_vj in neighbors[node[1]][tour]:
        if vi!=vj:
            if(node[0]==node[1]):
                sol,cost=func((node[0],),neighbors,solution,tour,vi,pos_vi,vj,pos_vj,func_2);
            else:
                sol,cost=func(node,neighbors,solution,tour,vi,pos_vi,vj,pos_vj,func_2);
            if (best_cost==None):
                best_cost=cost;
                best_sol=sol;
            elif (cost!=None and (cost[1]<best_cost[1])):
                best_cost=cost;
                best_sol=sol;
                    
    return best_sol,best_cost;

def geni_main(node,original_tour,neighbors,solution,func,func_2):
    best_sol=best_cost=cost=sol=None;
    #print(neighbors);
    for tour in neighbors[node[0]].keys():
        if(tour==original_tour):
            continue;
        for vi,pos_vi in neighbors[node[0]][tour]:
            #print(vi);
            #print(pos_vi);
            if not tour in neighbors[node[1]]:
                continue;
            sol,cost=geni_route(node,vi,pos_vi,tour,neighbors,solution,func,func_2);
            if (best_cost==None):
                best_cost=cost;
                best_sol=sol;
            elif (cost!=None and (cost[1]<best_cost[1])):
                best_cost=cost;
                best_sol=sol;
        #for vi,pos_vi in neighbors[node[0]][tour]:
        #    #print(vi);
        #    #print(pos_vi);
        #    if not tour in neighbors[node[1]]:
        #        continue;
        #    for vj,pos_vj in neighbors[node[1]][tour]:
        #        if vi!=vj:
        #            if(node[0]==node[1]):
        #                sol,cost=func((node[0],),neighbors,solution,tour,vi,pos_vi,vj,pos_vj,func_2);
        #            else:
        #                sol,cost=func(node,neighbors,solution,tour,vi,pos_vi,vj,pos_vj,func_2);
        #            if (best_cost==None):
        #                best_cost=cost;
        #                best_sol=sol;
        #            elif (cost!=None and (cost[1]<best_cost[1])):
        #                best_cost=cost;
        #                best_sol=sol;
                            
    return best_sol,best_cost;
    
def geni_type_I(node,original_tour,neighbors,solution):
    return geni_main(node,original_tour,neighbors,solution,geni_type_I_body,geni_route_type_I);

def geni_type_II(node,original_tour,neighbors,solution):
    return geni_main(node,original_tour,neighbors,solution,geni_type_II_body,geni_route_type_II);

def geni_type_I_inverted(node,original_tour,neighbors,solution):
    return geni_main(node,original_tour,neighbors,solution,geni_type_I_body,geni_route_type_I_inverse);

def geni_type_II_inverted(node,original_tour,neighbors,solution):
    return geni_main(node,original_tour,neighbors,solution,geni_type_II_body,geni_route_type_II_inverse);

def geni_route_I(node,vi,pos_vi,tour,neighbors,solution):
    return geni_route(node,vi,pos_vi,tour,neighbors,solution,geni_type_I_body,geni_route_type_I);

def geni_route_II(node,vi,pos_vi,tour,neighbors,solution):
    return geni_route(node,vi,pos_vi,tour,neighbors,solution,geni_type_II_body,geni_route_type_II);

def geni_route_I_inverted(node,vi,pos_vi,tour,neighbors,solution):
    return geni_route(node,vi,pos_vi,tour,neighbors,solution,geni_type_I_body,geni_route_type_I_inverse);

def geni_route_II_inverted(node,vi,pos_vi,tour,neighbors,solution):
    return geni_route(node,vi,pos_vi,tour,neighbors,solution,geni_type_II_body,geni_route_type_II_inverse);

def geni_insert(node,original_tour,neighbors,solution):
    
    best_sol=best_cost=None;
    first_iteration=True;
    
    for insertion in [geni_type_I,geni_type_I_inverted,
                      geni_type_II,geni_type_II_inverted
                      ]:
        sol,cost=insertion(node,original_tour,neighbors,solution);
        #sys.exit();  
        if(best_cost==None) or (cost!=None and (cost[1]<best_cost[1])):
            best_cost=cost;
            best_sol=sol;
            first_iteration=False;
    
    #print(best_sol,best_cost);
      
    return best_sol,best_cost;
    
    
    
def us_route_type_I(route,node,pos_vi,pos_vj,pos_vk,viplus,vjplus,vkplus,l):
    #print('us_type_I');
    #print(node,pos_vi,pos_vj,pos_vk,viplus,vjplus,vkplus);
    #print(route);
    route=geni_reverse(route,pos_vj,viplus)+geni_reverse(route,pos_vk,vjplus)+geni_straight(route,vkplus,pos_vi);
    route.remove(node[0]);
    #print(route);
    #print(route.index(node[0]));
    
    assert(len(route)==(l-len(node)));
    return route;

def us_route_type_I_inverse(route,node,pos_vi,pos_vj,pos_vk,viplus,vjplus,vkplus,l):
    #print(route);
    route=us_route_type_I(route,node,pos_vi,pos_vj,pos_vk,viplus,vjplus,vkplus,l);
    #print(route);
    route.reverse();
    #print(route);
    return route;

def us_route_type_II(route,node,pos_vi,pos_vj,pos_vk,pos_vl,viplus,vjplus,vkplus,vlplus,l):
    #print('us_type_II');
    #print(node,pos_vi,pos_vl,pos_vj,pos_vk,viplus,vlplus,vjplus,vkplus);
    #print(route);
    route=geni_reverse(route,pos_vl,viplus)+geni_straight(route,vlplus,pos_vj)+geni_straight(route,vkplus,pos_vi)+geni_reverse(route,pos_vk,vjplus);
    route.remove(node[0]);
    #print(route);
    assert(len(route)==(l-len(node)));
    return route;
    
def us_route_type_II_inverse(route,node,pos_vi,pos_vj,pos_vk,pos_vl,viplus,vjplus,vkplus,vlplus,l):
    route=us_route_type_II(route,node,pos_vi,pos_vj,pos_vk,pos_vl,viplus,vjplus,vkplus,vlplus,l);
    route.reverse();
    #print(route);
    return route;    
    
def us_route_I(node,vi,pos_vi,tour,neighbors,solution):
    return geni_route(node,vi,pos_vi,tour,neighbors,solution,geni_type_I_body,us_route_type_I);

def us_route_II(node,vi,pos_vi,tour,neighbors,solution):
    return geni_route(node,vi,pos_vi,tour,neighbors,solution,geni_type_II_body,us_route_type_II);

def us_route_I_inverted(node,vi,pos_vi,tour,neighbors,solution):
    return geni_route(node,vi,pos_vi,tour,neighbors,solution,geni_type_I_body,us_route_type_I_inverse);

def us_route_II_inverted(node,vi,pos_vi,tour,neighbors,solution):
    return geni_route(node,vi,pos_vi,tour,neighbors,solution,geni_type_II_body,us_route_type_II_inverse);
    
def us_unstring(vertex,pos_vertex,tour,n,sol_2):
    best_sol=best_cost=None;
    #print(vertex);
    for insertion in [us_route_I,us_route_I_inverted,
                      us_route_II,us_route_II_inverted]:
        #print("iterazione");
        #print(sol_2[tour]['route']);
        sol_3,cost=insertion((vertex,vertex),vertex,pos_vertex[1],tour,n,sol_2);
        if(best_cost==None) or (cost!=None and (cost[1]<best_cost[1])):
            best_cost=cost;
            best_sol=sol_3;
    
    #print(sol_2);
    #print(best_sol); 
    #print(n);       
    for k in range(len(best_sol[tour]['route'])):
        node=best_sol[tour]['route'][k];
        #node_pos=(tour,k);
        #node_n=(node,k);
        for node_2 in n:
            if tour not in n[node_2]:
                continue;
            for q in range(len(n[node_2][tour])):
                if(n[node_2][tour][q][0]==node):
                    n[node_2][tour][q][1]=k;
            #print([vertex,pos_vertex[1]],n[node_2][tour]);
            if([vertex,pos_vertex[1]] in n[node_2][tour]):
                #print("vertex found");
                i=n[node_2][tour].index([vertex,pos_vertex[1]]);
                del n[node_2][tour][i];
    #print(n);
    return best_sol,n;
    
def us_string(vertex,tour,n,sol_2):
    best_sol=best_cost=None;
    for insertion in [geni_route_I,geni_route_I_inverted,
                      geni_route_II,geni_route_II_inverted]:
        
        for vi,pos_vi in n[vertex][tour]:
            #print(vi);
            #print(pos_vi);
            #if not tour in n[vertex[1]]:
            #    continue;
            sol_3,cost=insertion((vertex,vertex),vi,pos_vi,tour,n,sol_2);
            if(best_cost==None) or (cost!=None and (cost[1]<best_cost[1])):
                best_cost=cost;
                best_sol=sol_3;
    
    return best_sol,best_cost;
    
def geni_us(tmp_solution,tour,neighbors,gran_dist):
    best_sol=best_cost=None;
    n=deepcopy(neighbors);
    sol=deepcopy(tmp_solution);
    route=sol[tour]['route'];
    k=0;
    for vertex in route:
        sol_2=deepcopy(sol);
        n_2=deepcopy(n);
        #print("unstringing");
        #route_2=sol_2[tour]['route'];
        #print(sol_2);
        sol_2,n_2=us_unstring(vertex,[tour,k],tour,n_2,sol_2);
        #sol_2[tour]['route']=route_2;
        #us_update_n(n_2,new_vertex_pos,gran_dist);
        #print(sol_2);
        #print("stringing");
        sol_3,cost=us_string(vertex,tour,n_2,sol_2);
        if(best_cost==None) or (cost!=None and (cost[1]<best_cost[1])):
            best_cost=cost;
            best_sol=sol_3;
        
        k+=1;
        
    return best_sol,best_cost;