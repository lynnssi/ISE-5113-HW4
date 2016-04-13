"""
Tabu Search

Define the following for the search 

Neighborhood::: Single-flip neighborhood
Tabu Memory:::  Number of moves
Selection of Candidate List::: From neighborhood that doesn't include tabu solutions
Evaluation Function::: knapsack weight. Negative values if it is greater than the max allowable weight. Same function used in localSearch1.py
 Tabu Criterion: Whether an element at an index has been flipped
 Aspiration Criteria::  If a tabu solution encountered at the current iteration is better than the best solution found so far, then its tabu status is overridden 
 choice of tabu tenure:: 5
 Stopping criterion: number of iterations...I would like to use something better

"""

import copy
from random import Random
import numpy as np

seed = 12345
myPRNG = Random(seed)

#initialize variables for general knapsack problem
values = []
weights = []

n = 100
maxWeight = 4*n

#initialize tabu search settings
stopping_criterion = True
tabu_tenure = 5
memory = {}

Best_Solution = None
Best_Value = None

"""
Initialize Knapsack problem
Define standard functions for knapsack problem
"""

def create_random_instance():
    #create values
    for i in xrange(0,n):
        values.append(myPRNG.randint(10,100))

    #create weights
    for i in xrange(0,n):
        weights.append(myPRNG.randint(5,15))

    #initialize starting current solution
    x_curr = []

    for i in xrange(0,n):              
        if myPRNG.random() < 0.7:
            x_curr.append(0)
        else:
            x_curr.append(1)   
    return x_curr

def calc_weight(x):
    a=np.array(x)
    c=np.array(weights)
    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection
    return totalWeight

def evaluate(x):

    a=np.array(x)
    b=np.array(values)

    value = np.dot(a,b)          
    totalWeight = calc_weight(x) 

    if totalWeight > maxWeight:
        value =  maxWeight - totalWeight

    return value


"""
Then define functions for Tabu Search
"""
#function to create a 1-flip neighborhood of solution x
def get_neighbors(solution):
    nbrhood = []     

    for i in xrange(0,n):
        nbrhood.append(solution[:])
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1

    return nbrhood    

#Find and return list of candidate moves, a subset of the neighborhood of current solution
#returns a list of tuples, each tuple is structured as (Solution, Index Flipped)

def get_candidate_moves(current):
    candidates = []     

    for i in xrange(0, n):    
        if i not in memory.keys():
            candidates.append((current[:], i))
            lastIndex = len(candidates) - 1
            if candidates[lastIndex][0][i] == 1:
                candidates[lastIndex][0][i] = 0
            else:
                candidates[lastIndex][0][i] = 1

    return candidates 


#return the candidate in the list that returns the extended cost function
#solution_list is a list of tuples structured as (Solution, Index Flipped)
def min_cost_solution(solution_list):

    #initialize values
    bestsol = solution_list[0][0]
    bestval = evaluate(solution_list[0][0])
    flipped_index = 0

    #check for best solution
    for sol in solution_list:
        val = evaluate(sol[0])
        if val > bestval:
            bestsol, bestval, flipped_index = sol[0], val, sol[1]

    return bestsol, flipped_index


#index of flipped position of the new solution to the tabu memory and updates the tabu memory
def update_tabu_memory(current_flipped_index):    

    for key in memory.keys():

        #If the memory, is greater than 1, decrement the memory by 1
        if memory[key] > 1:
            memory[key] = memory[key] - 1

        #If the memory for the key equals 1, remove the key from the dictionary
        else:
            memory.pop(key) 

    # Make new solution tabu-active
    memory[current_flipped_index] = tabu_tenure


"""
Implement Tabu Search
"""

iterations = 0 #for stopping criterion
current = create_random_instance()

while stopping_criterion: 
    candidate_moves = get_candidate_moves(current) #list of tuples (Solution, flipped index)
    current = min_cost_solution(candidate_moves) #tuple (Solution, flipped index)
    update_tabu_memory(current[1])
    current = current[0] #extract list from current and assign to current

    #check if new solution is better than the best solution found so far
    currentval = evaluate(current)
    if currentval > Best_Value:
        Best_Solution, Best_Value = current, currentval    

    #update stopping criterion if met
    if iterations >= 50:              #changed to 50, which outputs correct values and increases speed
        stopping_criterion = False
    else:
        iterations += 1

print "The best solution found is: ", Best_Solution 
print "Number of iterations: ", iterations
print "With value: ", Best_Value
print "The weight is: ", calc_weight(Best_Solution)