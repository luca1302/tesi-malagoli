__author__="davide"
__date__ ="$1-ago-2010 14.18.26$"

from customer import *
from trucks import *
from dima import *

def __change_format(routes,trucks):
    solution={};
    for r in range(len(routes)):
        l=len(routes[r]);
        for k in range(depot+1,l):
            customer=routes[r][k];
            customer_object=customers[customer];
            solution[customer]=AttributeList(customer,customer_object,get_truck_index(trucks[r]),trucks[r].max_load);

        depot_object=customers[depot];
        previous_delta_time_w=previous_delta_distance=previous_delta_load=0;
        total_load=0;
        truck_time=total_distance=elma[depot][routes[r][1]];

        for k in range(depot+1,l):
            customer_id=routes[r][k];
            customer=solution[customer_id];
            customer.succ=routes[r][(k+1)%l];
            customer.prec=routes[r][(k-1)%l];
            customer.truck_arrival_time=truck_time;
            customer.distance_from_next=elma[customer_id][customer.succ];
            truck_time=customer.truck_departure_time=max(truck_time,customer.opening) +customer.service_time;

            total_load+=customer.demand;
            customer.delta_load=max(0,total_load-customer.truck_max_load);
            customer.delta_distance=max(0,total_distance-depot_object.time_frame);
            total_distance+=customer.distance_from_next;
            customer.delta_time_window=max(0,customer.truck_departure_time-customer.closing);
            
            

    return solution;

def dummy_solution(customers,max_routes):
    """
        Build a dummy solution for the VRPTW with max_routes or less routes

        PARAMETERS:

        max_routes: the maximum number of routes to be found
        customers: the set of customers to use for routing
    """
    assert(type(customers)==type(set()));
    for value in customers:
        assert(type(value)==type(int()));
    assert(type(max_routes)==type(int()));

    
    routes=[[depot]];

    #index starts from 0, not 1
    k=0;
    max_routes=max_routes-1;
    truck=allocate_truck();
    trucks=[truck];

    for customer in customers:
        distances=__calculate_distances(routes[k],customer);
        if __costraint_violated(routes[k],customer,truck,distances):
            #print("costraint violated!");
            if k!=max_routes:
                #print("creating new route!");
                routes.append([depot]);
                trucks.append(allocate_truck());
                distances=__calculate_distances(routes[k+1],customer);
                
            k=min(k+1,max_routes);
            truck=trucks[k];
            #print("inserting customer in route {0}".format(k));
        __insert(routes[k],customer,distances,truck);

    #print(routes);
    return __change_format(routes,trucks);

def __calculate_distances(route,customer):
    distances={};
    if len(route)!=1:
        #print(len(route));
        #print(route);
        for k in range(len(route)-1):
            #print(k);
            distance=elma[route[k]][customer]+elma[customer][route[k+1]]+download_time(customer);
            distances[distance]=(route[k],route[k+1]);
    
        distance=elma[route[-1]][customer]+elma[customer][route[0]]+download_time(customer);
        distances[distance]=(route[-1],route[0]);
    else:
        distance=elma[route[0]][customer]+elma[customer][route[0]]+download_time(customer);
        distances[distance]=(None,None);
    return distances;

def __costraint_violated(route,customer,truck,distances):
    """
        Verify costrint violation in the route if the customer is added

        PARAMETERS:
        route: a list of Customer, is the route to check
        customer: a Customer to insert in the route
        truck: the used truck
        distances: extra distance for insertion solutions of the customer
    """
    assert(type(route)==type(list()));
    for value in route:
        assert(type(value)==type(int()));
    assert(type(customer)==type(int()));
    assert(type(truck)==type(Truck()));

    return ((__truck_max_load_violated(customer,truck)) or (__route_max_duration_violated(route,customer,distances,truck)));

def __truck_max_load_violated(customer,truck):
    """

    """
    #print(customers[customer].demand);
    #print(truck.load);



    #if((customers[customer].demand+truck.load)>(truck.max_load)):
    #    print("customer {0} violates truck load! (demand={1},load={2},max_load={3})".format(customer,customers[customer].demand,truck.load,truck.max_load));
    #else:
    #    print("customer {0} does not violates truck load (demand={1},load={2},max_load={3})".format(customer,customers[customer].demand,truck.load,truck.max_load));

    return ((customers[customer].demand+truck.load)>(truck.max_load));

def __route_max_duration_violated(route,customer,distances,truck):
    distance=__delta_time_distance(route,customer,distances);
    distance+=truck.time_frame;

    #if (distance>customers[route[0]].time_frame):
    #    print("customer {0} violates truck frame! (truck_time_frame={1},distance={2},depot_frame={3})".format(customer,truck.time_frame,distance,customers[route[0]].time_frame));
    #else:
    #    print("customer {0} does not violate truck frame (truck_time_frame={1},distance={2},depot_frame={3})".format(customer,truck.time_frame,distance,customers[route[0]].time_frame));
    return (distance>customers[route[0]].time_frame);

def __delta_time_distance(route,customer,distances):
    distance=min(distances.keys());
    #for k in range(len(route)):
    #    distance+=elma[route[k]][route[k+1]]+__download_time(route[k]);
    if(distances[distance][0]==route[-1]):
        distance+=elma[customer][route[0]];
    else:
        distance+=elma[route[-1]][route[0]];

    return distance;

def __insert(route,customer,distances,truck):
    """
        Verify costrint violation in the route if the customer is added

        PARAMETERS:
        route: a list of Customer, is the route to check
        customer: a Customer to insert in the route
    """
    assert(type(route)==type(list()));
    for value in route:
        assert(type(value)==type(int()));
    assert(type(customer)==type(int()));

    #print(distances);
    min_distance=min(distances.keys());
    delta_distance=__delta_time_distance(route,customer,distances);
    cust=distances[min_distance][0];
    #print("distances={0},min_distance={1},cust={2}".format(distances,min_distance,cust));

    if(cust==None):
    #    print("customer is the first of the route! (after the depot)");
        route.append(customer);
    elif(cust==route[-1]):
    #    print("customer must be inserted last!");
        route.append(customer);
    else:
        index=route.index(cust);
    #    print("customer must be inserted at index {0}".format(index));
        route[index+1:index+1]=[customer];

    truck.load+=customers[customer].demand;
    truck.time_frame+=delta_distance;
    #print("truck_load={0}/{1},truck_time_frame={2}/{3}".format(truck.load,truck.max_load,truck.time_frame,customers[route[0]].time_frame));
    #print(route);
    