"""Travelling salesman using Genetic Algorithm"""

from scipy import *
from numpy import *
import matplotlib.pyplot as plt	
from geopy.geocoders import Nominatim
import random

class City:
    def __init__(self , x, y,name): #initializing obj of the City
        self.x = x
        self.y = y
        self.name = name
    
    def __repr__(self):
        return self.name + " (" + str(self.x)+ " , " + str(self.y) + " )"
    
    #distance of a city from any city C
    def get_distance(self ,City C):
        return (sqrt((C.x - self.x)**2 +(C.y - self.y)**2))



#find euclidean distance (P1,P2)
def distance(P1 ,P2):
	if(P1 == P2):
		return 0.0
	d = sqrt((P1[0]-P2[0])**2 + (P1[1] - P2[1])**2)
	return d
#total distance (P,seq) of all the cities
##P is the array of points of the cities  we have given in the text file
## seq is the sequence of the cities followed by the travelling salesman
def get_total_distance(P, route):
	dist = 0.0
	n = len(route)
	for i in range(n-1):
		dist += distance(P[route[i]] , P[route[i+1]])
	dist += distance(P[route[n-1]] , P[route[0]]) #connecting last cities
	return dist

#read cities
def read_cities(PNames):
	P=[] #co-oridnates of cities
	j = 0
	
	
	geolocator = Nominatim(user_agent = "VID_GEO_APP")
	j=0
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
			P.insert(City(x,y,city))
                  
			PNames.insert(j,city)
			j+=1
	return P

#fitness class
class Fitness:
      #default constructor
    def __init__(self , route):
        self.route = route
        self.distance = 0.0
        self.fitness = 0.0

    def route_distance(self):
        self.distance = get_total_distance(self.route)
	
    def get_fitness(self):
		d = route_distance(self)
		self.fitness = 1.0/d
		return self.fitness
	
#to create initial population we will use ranodom sampling 

def create_route(P):# p is city list
	route = random.sample(P , len(P))

def initial_popualtion(pop_size , P):
	population = []
	for i in range( 0 , pop_size):
		population.append(create_route(P))
	return population

#to sort population according to the fitness
def rank_routes(population):
	fitness_result = {}#ordered set
	for i in range (0 , len(population)):
		fitness_result[i] = Fitness(population[i]).get_fitness()
	return sorted(fitness_result.items() , key=operator.itemgetter(1) , reverse=true)


#tuning parameter is after sorting retain 85% of the population
#then choose 1st parent as the strongest and 2nd randomly from the population 
#let them mate and produce children (approx 30%)
#sort the children by fitness and consider 50% of them (i.e. 15%) which become part of the population

#chance of mutation
# r = random number 
#mutation probability  = 0.04
#if (r > 1-0.04) mutation is allowed
# else proceed , No mutation

# to code gene crossover 
#create empty child list
#choose range between 2 cities from parent 2 and copy to child then copy remaining cities from parent 1

        

