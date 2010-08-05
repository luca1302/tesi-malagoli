# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="davide"
__date__ ="$2-ago-2010 0.45.33$"


__trucks_load_index={};

class Truck:
    def __init__(self,max_load=-1):
        self.__max_load=max_load;
        self.__load=0;
        self.__time_frame=0;
        if(max_load!=(-1)):
            if(max_load not in globals()['__trucks_load_index']):
                globals()['__trucks_load_index'][max_load]=[self];
            else:
                globals()['__trucks_load_index'][max_load].append(self);

    def get_load(self):
        return self.__load;

    def set_load(self,load):
        self.__load=load;

    def get_time_frame(self):
        return self.__time_frame;

    def set_time_frame(self,time_frame):
        self.__time_frame=time_frame;

    def get_max_load(self):
        return self.__max_load;

    def __mul__(self,n):
        #print(self);
        #print(n);
        return [Truck(self.max_load) for k in range(n)];

    load=property(get_load,set_load);
    time_frame=property(get_time_frame,set_time_frame);
    max_load=property(get_max_load);

def allocate_truck():
    load_max=max(__trucks_load_index.keys());
    truck=__trucks_load_index[load_max].pop();
    #print(truck);
    return truck;

def trucks_number():
    return len(__trucks);




__trucks=set(
Truck(200)*10

);