# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$2-ago-2010 1.30.50$"

depot=0;
download_cost_factor_1=2;
download_cost_factor_2=3;

class Customer:
    #__x;
    #__y;
    #__demand;

    def __init__(self,demand=0,a=0,e=0,x=0,y=0):
        self.__x=x;
        self.__y=y;
        self.__demand=demand;
        self.__a=a;
        self.__e=e;

    def set_x(self,x):
        self.__x=x;

    def get_x(self):
        return self.__x;

    def get_demand(self):
        return self.__demand;

    def set_demand(self,demand):
        self.__demand=demand;

    def get_time_frame(self):
        return self.__e-self.__a;
    
    x=property(get_x,set_x);
    demand=property(get_demand,set_demand);
    time_frame=property(get_time_frame);

def download_time(customer):
    return customers[customer].demand/download_cost_factor_1+customers[customer].demand/download_cost_factor_2;

customers=[Customer(15,0,24),Customer(3,0,24)];