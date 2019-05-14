###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: kiana hosseini
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    with open(filename) as f:
        cow_set={}
        for line in f:
            cow_info = line.strip().split(",")
            cow_set[cow_info[0]] = int(cow_info[1])
    
    return cow_set


# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    #sort cows by weight
    sorted_cows = sorted(cows.items(), key = lambda x : x[1], reverse = True)
    #list to contain all trips
    cow_transport = []
    trip_number = 0
    
    while sorted_cows:
        #initiate a new trip while there are cows remaining
        cow_transport.append([])
        total_weight = 0
        remaining_cows = []
        
        #iterate through cows and add them to trip if it doesn't exceed weight limit
        #otherwise add the cow to remaining cows list for next trip
        
        for index,value in enumerate(sorted_cows): 
            if total_weight + sorted_cows[index][1] <= limit:
                cow_transport[trip_number].append(sorted_cows[index][0])
                total_weight += sorted_cows[index][1]
            else:
                remaining_cows.append(sorted_cows[index])
        
        #update variables for next trip        
        trip_number += 1
        sorted_cows = remaining_cows
            
            
    return cow_transport
            
                
# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    
    trip_options = get_partitions(cows)
    best_option = None
    fewest_trips = len(cows)
    
    for option in trip_options:
        valid = True
        #check to see if individual trips in each option don't exceed weight limit
        for trip in option:
            weight = sum(list(map(lambda x : cows[x] , trip)))
            if weight>limit:
                valid = False
                break
        #compare to best option so far, and replace if fewer number of trips
        if valid:
            if len(option)<=fewest_trips:
                best_option = option
                fewest_trips = len(option)
                
    return best_option        
            
    
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cow_set = load_cows("ps1_cow_data.txt")
    
    def get_run_time(func):
        start = time.time()
        print(func(cow_set))
        end = time.time()
        return end-start
        
    greedy_time = get_run_time(greedy_cow_transport)
    brute_force_time = get_run_time(brute_force_cow_transport)
    
    print("---"*20)
    print("greedy runtime: ",greedy_time)
    print("brute force runtime: ", brute_force_time)

#compare_cow_transport_algorithms()
print(brute_force_cow_transport({'Betsy': 65, 'Daisy': 50, 'Buttercup': 72}, 75))
