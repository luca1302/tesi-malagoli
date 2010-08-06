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
    #return customers[customer].demand/download_cost_factor_1+customers[customer].demand/download_cost_factor_2;
    return 90;

customers=[
Customer(0.00,0,1236),
Customer(10.00,912,967),
Customer(30.00,825,870),
Customer(10.00,65,146),
Customer(10.00,727,782),
Customer(10.00,15,67),
Customer(20.00,621,702),
Customer(20.00,170,225),
Customer(20.00,255,324),
Customer(10.00,534,605),
Customer(10.00,357,410),
Customer(10.00,448,505),
Customer(20.00,652,721),
Customer(30.00,30,92),
Customer(10.00,567,620),
Customer(40.00,384,429),
Customer(40.00,475,528),
Customer(20.00,99,148),
Customer(20.00,179,254),
Customer(10.00,278,345),
Customer(10.00,10,73),
Customer(20.00,914,965),
Customer(20.00,812,883),
Customer(10.00,732,777),
Customer(10.00,65,144),
Customer(40.00,169,224),
Customer(10.00,622,701),
Customer(10.00,261,316),
Customer(20.00,546,593),
Customer(10.00,358,405),
Customer(10.00,449,504),
Customer(20.00,200,237),
Customer(30.00,31,100),
Customer(40.00,87,158),
Customer(20.00,751,816),
Customer(10.00,283,344),
Customer(10.00,665,716),
Customer(20.00,383,434),
Customer(30.00,479,522),
Customer(20.00,567,624),
Customer(10.00,264,321),
Customer(10.00,166,235),
Customer(20.00,68,149),
Customer(10.00,16,80),
Customer(10.00,359,412),
Customer(10.00,541,600),
Customer(30.00,448,509),
Customer(10.00,1054,1127),
Customer(10.00,632,693),
Customer(10.00,1001,1066),
Customer(10.00,815,880),
Customer(10.00,725,786),
Customer(10.00,912,969),
Customer(20.00,286,347),
Customer(40.00,186,257),
Customer(10.00,95,158),
Customer(30.00,385,436),
Customer(40.00,35,87),
Customer(30.00,471,534),
Customer(10.00,651,740),
Customer(20.00,562,629),
Customer(10.00,531,610),
Customer(20.00,262,317),
Customer(50.00,171,218),
Customer(10.00,632,693),
Customer(10.00,76,129),
Customer(10.00,826,875),
Customer(10.00,12,77),
Customer(10.00,734,777),
Customer(10.00,916,969),
Customer(30.00,387,456),
Customer(20.00,293,360),
Customer(10.00,450,505),
Customer(10.00,478,551),
Customer(50.00,353,412),
Customer(20.00,997,1068),
Customer(10.00,203,260),
Customer(10.00,574,643),
Customer(20.00,109,170),
Customer(10.00,668,731),
Customer(10.00,769,820),
Customer(30.00,47,124),
Customer(20.00,369,420),
Customer(10.00,265,338),
Customer(20.00,458,523),
Customer(30.00,555,612),
Customer(10.00,173,238),
Customer(20.00,85,144),
Customer(30.00,645,708),
Customer(10.00,737,802),
Customer(10.00,20,84),
Customer(10.00,836,889),
Customer(20.00,368,441),
Customer(40.00,475,518),
Customer(10.00,285,336),
Customer(30.00,196,239),
Customer(10.00,95,156),
Customer(30.00,561,622),
Customer(20.00,30,84),
Customer(10.00,743,820),
Customer(20.00,647,726),
];
