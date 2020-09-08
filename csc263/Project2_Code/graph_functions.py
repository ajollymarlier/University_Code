# Assume we have adjacency matrix "adj_mat" that stores weight_key_pair objects, uses python lists
# Assume dictionary "car_dict" exists as (<int> id, <Car> object) setup, where key is unique id
# Assume list "restaurants" stores Restaurant objects with same index as row in adj_mat
List[List[Weight_Key_Pair]] adj_mat
dict car_dict(<int>, <Car>)
List[Restaurant] restaurants

class Car:
    int id
    string driver_name
    double avg_rating
    string license_plate


class Restaurant:
    double longitude
    double latitude
    string name
    double avg_rating


class Weight_Key_Pair:
    int id
    int drive_time


def addCar(Car c):
    for r_index in range(0, len(adj_mat)):
        curr_restaurant = restaurants[r_index]
        adj_mat[r_index].append(Weight_Key_Pair(c.id, ceil(getDrivingTime(curr_restaurant, c)))) #Assumes we have external function that provides 
                                                                                                 #estimated driving time from Car c to Restaurant r
        car_dict[c.id] = c                                                                       


def removeCar(Car c):
    bool found = False

    for c_index in range(0, len(adj_mat[0])):
        target_id = adj_mat[0][i]

        if car_dict[target_id].id = c.id:
            for(r_index in range(0, len(adj_mat)):
                del adj_mat[r_index][c_index]

            found = True
            break
    
    if found:
        del car_dict[c.id]
    else:
        raise Exception
    


def addRestaurant(Restaurant r):
    adj_mat.append([])

    for i in range(0, len(adj_mat[0])):
        curr_car_id = adj_mat[0][i].id
        curr_car = car_dict[curr_car_id]

        adj_mat[len(adj_mat) - 1].append(Weight_Key_Pair(curr_car.id, ceil(getDrivingTime(r, curr_car))))

        restaurants.append(r)


def removeRestaurant(Restaurant r):
    bool found = False

    for r_index in range(0, len(adj_mat)):
        if(restaurants[r_index] == r):
            del adj_mat[r_index]
            del restaurants[r_index]
            found = True
            break
    
    if not found:
        raise Exception



def delivery(Restaurant r, int cook_time):
    bool found = False
    for r_index in range(0, len(adj_mat)):
        if restaurants[r_index] == r:
            restaurants[r_index] = sort(restaurants[r_index], len(restaurants[r_index]), cook_time)
            found = True

            closest_cars = []
            for i in range(0, 3):
                closest_cars.append(restaurants[r_index][i])

            return closest_cars
    
    if not found:
        raise Exception


#Helper function
#Reference: https://www.geeksforgeeks.org/merge-sort/
def sort(List[Weight_Key_Pair] arr, int cook_time) : #returns List[Weight_Key_Pair]
    if len(arr) >1: 
        pivot = randint(1, n-1)  # Finding the mid of the array 
        L = arr[:pivot] # Dividing the array elements  
        R = arr[pivot:] # into 2 halves 
  
        mergeSort(L) # Sorting the first half 
        mergeSort(R) # Sorting the second half 
  
        i = j = k = 0
          
        # Copy data to temp arrays L[] and R[] 
        while i < len(L) and j < len(R): 
            if abs(L[i].drive_time - cook_time) < abs(R[j].drive_time - cook_time): 
                arr[k] = L[i] 
                i+= 1
            else: 
                arr[k] = R[j] 
                j+= 1
            k+= 1
          
        # Checking if any element was left 
        while i < len(L): 
            arr[k] = L[i] 
            i+= 1
            k+= 1
          
        while j < len(R): 
            arr[k] = R[j] 
            j+= 1
            k+= 1


def setEdge(Car c, Restaurant r, int new_time):
    bool found = False
    for r_index in range(0, len(adj_mat)):
        if r == restaurants[r_index]:

            for c_index in range(0, len(adj_mat[0])):
                curr_car_id = adj_mat[r_index][c_index].id

                if car_dict[curr_car_id] == c:
                    adj_mat[r_index][c_index].drive_time = new_time
                    found = True
    
    if not found:
        raise Exception


def getEdge(Car c, Restaurant r):
    bool found = False
    for r_index in range(0, len(adj_mat)):
        if r == restaurants[r_index]:

            for c_index in range(0, len(adj_mat[0])):
                curr_car_id = adj_mat[r_index][c_index].id

                if car_dict[curr_car_id] == c:
                    return adj_mat[r_index][c_index].drive_time
    
    if not found:
        raise Exception


def getCars():
    return list(car_dict.values())


def getRestaurants():
    return restaurants

