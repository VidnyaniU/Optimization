"""Travelling Salesman using Simulated Annealing"""
from scipy import *
from numpy import *
import matplotlib.pyplot as plt	
from geopy.geocoders import Nominatim
import random

#find euclidean distance (P1,P2)
def distance(P1 ,P2):
	if(P1 == P2):
		return 0.0
	d = sqrt((P1[0]-P2[0])**2 + (P1[1] - P2[1])**2)
	return d

#total distance (P,seq) of all the cities
##P is the array of points of the cities  we have given in the text file
## seq is the sequence of the cities followed by the travelling salesman
def total_distance(P, seq):
	dist = 0.0
	n = len(seq)
	for i in range(n-1):
		dist += distance(P[seq[i]] , P[seq[i+1]])
	dist += distance(P[seq[n-1]] , P[seq[0]]) #connecting last cities
	return dist


#read cities 
def readCities(PNames):
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
			
			P.insert(j , [x, y])
			PNames.insert(j,city)
			j+=1
	return P


#plot the cities 
def plot_cities(seq, P, tot_dist, PNames):
    Pt = [P[seq[i]] for i in range(len(seq))]
    Pt += [P[seq[0]]]
    Pt = array(Pt)
    
    plt.figure()
    plt.title('Total Distance: ' + str(tot_dist))
    plt.plot(Pt[:, 0], Pt[:, 1], '-o')
    
    for i in range(len(P)):
        plt.annotate(PNames[i], (P[i][0], P[i][1]))
    
    plt.show()


#swap 2 cities
def swap(P,seq,dist,N1,N2,temp,num_of_cities):
	N1L = N1 -1
	if(N1L < 0):
		N1L += num_of_cities
	
	N1R = N1+ 1
	if (N1R >= num_of_cities):
		N1R =0

	N2L = N2 -1
	if(N2L < 0):
		N2L += num_of_cities
	
	N2R = N2 +1
	if (N2R >= num_of_cities):
		N2R =0


	I1 = seq[N1]
	I2 = seq[N2]
	I1L=seq[N1L]
	I1R = seq[N1R]
	I2L =seq[N2L]
	I2R = seq[N2R]
	
	delta = 0.0
	delta += distance(P[I1L],P[I2])
	delta += distance(P[I1],P[I2R])
	delta -= distance(P[I1L] , P[I1])
	delta -= distance(P[I2] , P[I2R])
	
	if(N1 != N2L and N1R != N2 and N1R != N2L and N2 != N1L):
		delta += distance(P[I2] , P[I1R])
		delta += distance(P[I2L] ,P[I1])
		delta -= distance(P[I1], P[I1R])
		delta -= distance(P[I2L] , P[I2])
	
	prob = 1.0
	if(delta > 0.0):
		prob = exp(-delta/temp)
	rndm = random.random()
	
	if(rndm < prob):
		dist += delta
		seq[N1] = I2
		seq[N2] = I1
		
		dif = abs(dist - total_distance(P, seq))
		if(dif*dist > 0.01):
			dist = total_distance(P,seq)
			#print 
			input("PRESS ENTER TO CONTINUE...")
		return dist,True
	else :
		return dist, False

	




#reverse 2 cities
def reverse(P,seq,dist,N1,N2,temp,num_of_cities):
	N1L = N1 -1
	if(N1L < 0):
		N1L += num_of_cities
	N2R = N2 +1
	if(N2R >= num_of_cities):
		N2R = 0
	
	delta = 0.0
	

	I1 = seq[N1]
	I2 = seq[N2]
	I1L=seq[N1L]
	I2R = seq[N2R]
	
	delta = 0.0

	
	if(N1 != N2R and N2 != N1L):
		delta += distance(P[I1L] , P[I2])
		delta += distance(P[I1] ,P[I2R])
		delta -= distance(P[I1L], P[I1])
		delta -= distance(P[I2] , P[I2R])
	else:
		return dist, False
	
	prob = 1.0
	if(delta > 0.0):
		prob = exp(-delta/temp)
	rndm = random.random()
	
	if(rndm < prob):
		dist += delta
		i = N1
		j= N2
		while(i < j):
			u =seq[i]
			seq[i] = seq[j]
			seq[j] = u
			i+=1
			j-=1
		
		dif = abs(dist - total_distance(P, seq))
		if(dif*dist > 0.01):
			dist = total_distance(P,seq)
			#print 
			input("PRESS ENTER TO CONTINUE...")
		return dist,True
	else :
		return dist, False

#main 
if __name__ == '__main__':
	PNames = []
	
	P= readCities(PNames)
	num_of_cities = len(P)
	
	maxTsteps = 250
	fCool=0.9
	maxSwaps = 2000
	maxAccepted = 10 * num_of_cities
	
	seq = arange(0,num_of_cities,1)
	
	tot_dist=total_distance(P, seq)
	temp = 10.0 * tot_dist
	#input("Press enter to continue....")
	plot_cities(seq , P, tot_dist,PNames)
	oldDist = 0.0
	convergenceCount = 0
	
	for t in range(1 , maxTsteps+1):
		if(temp < 1.0e-6):
			break
		accepted = 0
		iteration = 0

		while (iteration <= maxSwaps):
			N1 = -1
			while (N1 <0  or N1 >=num_of_cities):
				N1 = ((int) (random.random() * 1000.0))%num_of_cities
			N2 = -1
			while (N2 <0  or N2 >=num_of_cities or N2 == N1):
				N2 = ((int) (random.random() * 1000.0))%num_of_cities
			
			if(N2 <N1):
				N1 = N1 + N2
				N2 = N1 - N2
				N1 = N1 - N2

			chk = random.uniform(0,1)
			if((chk < 0.5) and (N1+1 != N2) and (N1 != ((N2+1)%num_of_cities))):
				tot_dist , flag = swap(P , seq , tot_dist , N1 , N2 , temp , num_of_cities)

			else:
				tot_dist , flag = reverse(P , seq , tot_dist , N1 , N2 , temp , num_of_cities)
			
			if(flag):
				accepted += 1
			iteration += 1
		print ("Iteration: %d temp :: %f dist :: %f" %(t, temp,tot_dist))
		print ("Seq :: " )
		set_printoptions(precision =3)
		print(seq)
		
		if(abs(tot_dist - oldDist) < 1.0e-4):
			convergenceCount += 1
		else:
			convergenceCount = 0
		if(convergenceCount >= 4):
			break
		if((t%25) == 0):
			plot_cities(seq , P, tot_dist , PNames)
		temp *= fCool
		oldDist = tot_dist

	plot_cities(seq , P ,tot_dist , PNames)































