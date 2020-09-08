import math

class Car_Node:
    int ID
    double drive_time_m
    Car_Node next_car

class Car:
    int ID
    string driver_name
    double avg_rating
    string licence_plate
    (int, int) location

class Restaurant:
    Car_Node lst_head
    string name
    double avg_rating
    Restaurant next_rest
    (int, int) location


#Global Variables
Restaurant rest_lst_head
HashTable(<int> ID, <Car> car) cars

def delivery(Restaurant r, Car c, int cook_time)
    cmpr_val = math.inf
    car_node_arr = [math.inf, math.inf, math.inf]

    curr_rest = rest_lst_head
    while(curr_rest != NULL):
        if(curr_rest == r):

            curr_car = r.lst_head
            while(curr_car != NULL):
                cmpr_val = abs(curr_car.drive_time_m - cook_time)

                if (cmpr_val < car_arr[2]):
                    temp = cmpr_val
                    cmpr_val = car_arr[2]
                    car_arr[2] = temp
                
                if (car_arr[2] < car_arr[1]):
                    temp = car_arr[1]
                    car_arr[2] = car_arr[1]
                    car_arr[1] = temp

                if (car_arr[1] < car_arr[0]):
                    temp = car_arr[0]
                    car_arr[1] = car_arr[0]
                    car_arr[0] = temp

                curr_car = curr_car.next_car

        curr_rest = curr_rest.next_rest
    
    final_arr = []
    final_arr[0] = cars[car_node_arr[0]]
    final_arr[1] = cars[car_node_arr[1]]
    final_arr[2] = cars[car_node_arr[2]]

    return final_arr


def addCar(Car c):
    curr_rest = lst_head
    while(curr_rest != NULL):
        curr_car_node = curr_rest.lst_head

        while(curr_car_node != NULL):
            if (curr_car_node.lst_head is NULL):
                curr_car_node.lst_head = Car_Node(c.ID)
                
            curr_car_node = curr_car_node.next_car

        curr_rest = curr_rest.next_rest

    cars[c.ID] = c


def removeCar(Car c):
    bool found = False

    curr_rest = rest_lst_head
    while(curr_rest != NULL):
        curr_car_node = curr_rest.lst_head

        while(curr_car_node.next_car != NULL):
            if (cars[curr_car_node.next_car.ID] == c):
                found = True
                temp = curr_car_node.next_car.next_car
                curr_car_node.next_car = temp

                del cars[c.ID]
                
            curr_car_node = curr_car_node.next_car

        curr_rest = curr_rest.next_rest
    
    if not found:
        raise Exception


#def addRestaurant(Restaurant r):
#    curr_rest = rest_lst_head
#    while(curr_rest != NULL):
#        if(curr_rest.next_rest is NULL):
#            curr_rest.next_rest = r
#            curr_new_car_node = NULL

#            curr_head_car_node = rest_lst_head.lst_head
#            while (curr_head_car_node != NULL):
#                curr_new_car_node = Car_Node(curr_head_car_node.ID, getDrivingTime(r, cars[curr_head_car_node.ID]), NULL)

                


#       curr_rest = curr_rest.next_rest
        
        

