"""Travelling salesman using Genetic Algorithm"""

import random
import operator
from scipy import *
import numpy as np 
import matplotlib.pyplot as plt	
from geopy.geocoders import Nominatim

class City:
    def __init__(self , x, y,name): #initializing obj of the City
        self.x = x
        self.y = y
        self.name = name
    
    def __repr__(self):
        return self.name + " (" + str(self.x)+ " , " + str(self.y) + " )"
    
    #distance of a city from any city C
    def get_distance(self ,city):
        return (np.sqrt((city.x - self.x)**2 +(city.y - self.y)**2))



#find euclidean distance (P1,P2)
# def distance(P1 ,P2):
# 	if(P1 == P2):
# 		return 0.0
# 	d = sqrt((P1[0]-P2[0])**2 + (P1[1] - P2[1])**2)
# 	return d

#total distance (P,seq) of all the cities
##P is the array of points of the cities  we have given in the text file
## seq is the sequence of the cities followed by the travelling salesman
def get_total_distance(route):
	dist = 0.0
	 
	for i in range(len(route)-1):
		dist += route[i].get_distance(route[i+1])
	dist += route[-1].get_distance(route[0]) #connecting last cities
	return dist

#read cities
def read_cities(PNames):
	P=[] #co-oridnates of cities
	j = 0
	geolocator = Nominatim(user_agent = "VID_GA_GEO_APP")
	with open("./India_cities.txt") as file:
		for line in file:
			city = line.rstrip('\n')
			if(city == ""):
				break
			
			city += ",India"
			pt = geolocator.geocode(city, timeout = 10000)
			y = round(pt.latitude , 2)
			x= round(pt.longitude , 2)
			#print("City[%2d]=%s(%5.2f , %5.2f)" % (j , city,x,y))
			
			# P.insert(j , [x, y])
			P.append(City(x,y,city))
                  
			PNames.append(city)
			j+=1
	return P

def plot_route(route, P, tot_dist, PNames):
    Pt = [[city.x, city.y] for city in route]
    Pt.append([route[0].x, route[0].y]) 
    Pt = np.array(Pt) 
    
    # Plot the cities and the route
    plt.figure()
    plt.title(f'Total Distance: {tot_dist:.2f}')
    plt.plot(Pt[:, 0], Pt[:, 1], '-o') 
    
    for i, city in enumerate(route):
        plt.annotate(city.name, (city.x, city.y), textcoords="offset points", xytext=(0,10), ha='center')
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.show()

#fitness class
class Fitness:
      #default constructor
    def __init__(self , route):
        self.route = route
        self.distance = 0.0
        self.fitness = 0.0

    def route_distance(self):
        if self.distance == 0:
            self.distance = get_total_distance(self.route)
        return self.distance

	
    def get_fitness(self):
        if self.fitness == 0:
            self.fitness = 1.0 / self.route_distance()
        return self.fitness
    
         
	
#to create initial population we will use random sampling 

def create_route(P):# p is city list
	return random.sample(P , len(P))
    

def initial_population(pop_size , P):
	population = []
	for i in range( 0 , pop_size):
		population.append(create_route(P))
	return population

# #to sort population according to the fitness
def rank_routes(population):
	fitness_result = {}#ordered set
	for i in range (0 , len(population)):
		fitness_result[i] = Fitness(population[i]).get_fitness()
	return sorted(fitness_result.items() , key=operator.itemgetter(1) , reverse=True)


#tuning parameter is after sorting retain 80% of the population
#then choose 1st parent as the strongest and 2nd randomly from the population 
#let them mate and produce children (approx 40%)
#sort the children by fitness and consider 50% of them (i.e. 20%) which become part of the population

#chance of mutation
# r = random number 
#mutation probability  = 0.04
#if (r > 1-0.04) mutation is allowed
# else proceed , No mutation

# to code gene crossover 
#create empty child list
#choose range between 2 cities from parent 2 and copy to child then copy remaining cities from parent 1

#selecting based on elitist population
def selection(ranked_population, elite_size):
    selection_result = []
    
    for _ in range(len(ranked_population)):
        individual = random.sample(ranked_population, elite_size) 
        best_individual = max(individual, key=lambda x: x[1])     # Selecting the fittest
        selection_result.append(best_individual[0])             

    return selection_result


def mating_pool(population , selection_result):
    mating_pool = []
    for i in range (len(selection_result)):
        mating_pool.append(population[selection_result[i]])
    return mating_pool

#crossover
#in case of TSP parent is the sequence of the cities and cities are genes which we are going to mix and match
def crossover(parent1 ,parent2):
    child_p1 = [] #genes from parent1
    child_p2 = [] #genes from parent2

    #determining the range of copying genes from parent1
    gene_a = int(random.random() * len(parent1))
    gene_b = int(random.random() * len(parent1))

    start_gene = min(gene_a , gene_b)
    end_gene =  max(gene_a , gene_b)

    #copying the genes from parent1
    for i in range(start_gene , end_gene):
        child_p1.append(parent1[i])
    
    child_p2 = [item for item in parent2 if item not in child_p1]

    return child_p1 + child_p2

#crossover to create next generation
def create_children(mating_pool , elite_size):
    children = []
    n = len(mating_pool) - elite_size
    pool = random.sample(mating_pool, len(mating_pool))

    for i in range(elite_size):
        children.append(mating_pool[i])
    
    for i in range(n):
        child  =crossover(pool[i] , pool[len(mating_pool) - i - 1])
        children.append(child)
    
    return children

#chance of mutation
# r = random number 
#mutation probability  = 0.04
#if (r < 0.01) mutation is allowed
# else proceed , No mutation

def mutation(individual , mutation_probability):
    for i in range(len(individual)):
        if random.random()  < mutation_probability:
            j = int(random.random()  * len(individual))

            #swapping the cities
            city1 = individual[i]
            city2 = individual[j]

            individual[i] = city2
            individual[j] = city1

    return individual

#apply mutation 
def mutate_population(population , mutation_probability):
    mutated_population =[]
    for individual in population:
        mutated_individual = mutation(individual ,mutation_probability)
        mutated_population.append(mutated_individual)
    return mutated_population

#next generation
def next_generation(current_generation , elite_size , mutation_probability):
    ranked_population = rank_routes(current_generation)
    selection_result = selection(ranked_population , elite_size)
    mating_pool_population = mating_pool(current_generation , selection_result)
    new_children = create_children(mating_pool_population , elite_size)
    next_generation = mutate_population(new_children , mutation_probability)

    return next_generation

def genetic_algorithm(pop_size , elite_size , mutation_probability , generations):
    P = read_cities(PNames)
    

    population = initial_population(pop_size , P)
    progress =[]
    old_distance = get_total_distance(population[0])
    print(f"Initial distance :: {old_distance}")
    progress.append(1/rank_routes(population)[0][1])

    for gen in range(1 , generations+1):
        population = next_generation(population , elite_size , mutation_probability)
        best_route_ind = rank_routes(population)
        best_route = population[best_route_ind [0][0]]

       
        progress.append(1 / best_route_ind[0][1]) #tracking progress


        #plotting every 10 generations
        if gen%25 ==0:
            new_distance = get_total_distance(best_route)
            print(f"Generation {gen} :: Distance = {new_distance}")
            plot_route(best_route , P ,new_distance ,PNames)

           
    
    best_route_ind = rank_routes(population)[0][0]
    best_route = population[best_route_ind]
    print(f"\nFinal distance = {get_total_distance(best_route)}\n")

    plot_route(best_route ,P,get_total_distance(best_route) ,PNames)

    #plotting the increase in avg. fitness from generation to generation
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.title('Distance over Generations')
    plt.show()

if __name__ == "__main__":
    PNames = []
    pop_size = 100
    elite_size = 20
    mutation_probability = 0.01
    generations = 200

    genetic_algorithm(pop_size , elite_size , mutation_probability , generations)
    
                           

