#simulated annealing
#boltzmann schedule
import copy
from random import Random
import numpy as np
import time         # needed for temperature dependent probability
import math         # needed for logarithm and exponent functions

#to setup a random number generator, we will specify a "seed" value
seed = 12345
myPRNG = Random(seed)

#let's create an instance for the knapsack problem
def create_random_instance(values, weights):
    #values = []
    for i in xrange(0,n):
        values.append(myPRNG.randint(10,100))
        
    #weights = []
    for i in xrange(0,n):
        weights.append(myPRNG.randint(5,15))
    
def calc_weight(x):
    a=np.array(x)
    c=np.array(weights)
    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection
    return totalWeight

#function to evaluate a solution x
def evaluate(x):
          
    a=np.array(x)
    b=np.array(values)
    #c=np.array(weights)
    
    value = np.dot(a,b)          #compute the cost value of the knapsack selection
    totalWeight = calc_weight(x) #np.dot(a,c)    #compute the weight value of the knapsack selection
    
    if totalWeight > maxWeight:
        value =  maxWeight - totalWeight
        #value = -1
    
    return value
          
#function to create a 1-flip neighborhood of solution x         
def neighborhood(x):
    nbrhood = []     
    
    for i in xrange(0,n):
        nbrhood.append(x[:])
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1
    
    return nbrhood
          
#boltzmann cooling schedule
def boltzmann(initialTemp, k):
    temp = initialTemp / math.log(1+k, 10)
    
    return temp

#random variables set by programmer needed for simulated annealing 
initialTemp = 100   
tempLength = 30
maxLength = 60

#number of elements in a solution
n = 500

#define max weight for the knapsack
maxWeight = 4*n

#monitor the number of solutions evaluated
solutionsChecked = 0
totalNumIterations = 0
      
#initialize values and weights
values = []
weights = []
create_random_instance(values, weights)

#define the solution variables
x_curr = [] #x_curr will hold the current solution 

#start with a random solution
for i in xrange(0,n):
    #x_curr.append(myPRNG.randint(0,1))
    
    if myPRNG.random() < 0.7:
        x_curr.append(0)
    else:
        x_curr.append(1)

#begin local search overall logic
done = 0

x_best = x_curr[:]   #x_best will hold the best solution 
f_curr = evaluate(x_curr)  #f_curr will hold the "fitness" of the current soluton 
f_best = f_curr
    
#simulated annealing loop (stopping criterion is the max length)
for k in range(1, maxLength+1):
    #counter variable 
    counter = 0
    
    #sets the temperature 
    temp = boltzmann(initialTemp, k)
    
    Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr
    
    #this loops until counter == tempLength, then exits function back into the for loop
    #where the temp gets set again, and the process continues for each temp value
    while counter < tempLength:
        c = myPRNG.choice(Neighborhood)
        totalNumIterations = totalNumIterations + 1
        
        if evaluate(c) > f_best:   
            x_best = c[:]              #find the best member and keep track of that solution
            f_best = evaluate(c)       #and evaluation value
    
        else:
            #objective values difference
            change = evaluate(x_curr) - evaluate(c)
            
            epsilon = myPRNG.uniform(0,1)
            
            if epsilon <= math.exp(-1*change/temp):   #from lecture 17, slide 494
                x_curr = x_best[:]         #else: move to the neighbor solution and continue
                f_curr = f_best            #evaluate the current solution
        
        # just to keep track of the temp as it 'cools'
        # will maxlength+1 times, then repeat for a lower temp
        print "Current Temperature %.2f" % temp      
        # increase counter by one
        counter = counter + 1
        solutionsChecked += 1

print "\nWeight of knapsack: ", calc_weight(x_best)
print "Best value found: ", f_best
print "Best solution: ", x_best
print "Total Count: ", counter      #this should equal the tempLength variable
print "tempLength: ", tempLength    #this should equal the counter variable
print "Final Temperature %.2f" % temp 
print "Solutions Checked", solutionsChecked
