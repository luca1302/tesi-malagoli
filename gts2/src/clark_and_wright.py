# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$3-ago-2010 16.32.33$"

from copy import *
from customer import *

def __sorting(x):
    #print(x);
    #print(len(x));
    return len(x);

class Clark_and_Wright():

    def __init__(self,dima,elma,customers,allocate_truck,trucks_number,depot_index):
        self.__dima=dima;
        self.__elma=elma;
        self.__customers=customers;
        self.__allocate_truck=allocate_truck;
        self.__truck_number=trucks_number;
        self.__depot_index=depot_index;
        self.__savings={};
        self.__routes={};
        self.__max_truck=allocate_truck();
        self.__max_capacity=self.__max_truck.max_load;
        #print(customers);
        #customers=deepcopy(customers);
        #customers=customers-customers[depot_index];
        scan=range(len(customers));
        for i in scan:
            self.__routes[i]=[i];
            for j in scan:
                saving=dima[i][depot_index]+dima[depot_index][j]-dima[i][j];
                couple=(i,j);
                if saving in self.__savings:
                    self.__savings[saving].append(couple);
                else:
                    self.__savings[saving]=[couple];
        
    def is_feasible(self,list):
        depot_object=customers[self.__depot_index];
        total_load=0;
        total_time=depot_object.opening;
        prev_index=self.__depot_index;
        for index in list:
            customer=self.__customers[index];
            total_load+=customer.demand;
            total_time+=self.__elma[prev_index][index];
            total_time=max(total_time,customer.opening)+download_time(index);
        total_time+=self.__elma[len(list)-1][self.__depot_index];
        
        return ((total_load<self.__max_capacity) and (total_time<depot_object.time_frame));
    
    def find_starting_solution(self):
        savings=self.__savings.keys();
        sorted(savings,reverse=True);
        l=len(savings);
        for k in range(l):
            for saving in self.__savings[k]:
                for couple in self.__savings[saving]:
                    if((couple[0] in self.__start) and (couple[1] in self.__end)):
                        route_2=self.__start[couple[0]];
                        route=self.__end[couple[1]];
                        
                    elif((couple[0] in self.__end) and (couple[1] in self.__start)):
                        route_2=self.__start[couple[1]];
                        route=self.__end[couple[0]];
                    
                    if is_feasible(route+route2):
                        self.__routes[route]+=route_2;
                        del self.__routes[route_2];
                    
                        for dictionary in [self.__start,self.__end]:
                            for element,r in dictionary:
                                if r==route_2:
                                    del dictionary[element];
        
        if(len(self.__routes.keys())>self.__truck_number):
            routes=[];
            for key,route in self.__routes:
                routes.append(route);
            sorted(routes,key=__sorting,reverse=True);
            k=0;
            t=self.__truck_number;
            for route in range(t,len(routes)):
                routes[k]+=route;
                k=(k+1)%t;
            self.__routes=routes;
                 
        
        solution=[];
        for key,route in self.__routes:
            tour={};
            tour['truck']=self.__max_truck;
            self.__max_truck=self.__allocate_truck();
            tour['route']=route;
            tour['new_tabu']={};
            tour['inserted']={};
            tour['deleted']={};
            tour['old_tabu']={};
            solution.append(tour);
        return solution;