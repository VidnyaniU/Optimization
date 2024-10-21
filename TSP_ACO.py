import numpy as np
import random
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim

#Setting  Parameters
alpha = 1.0  # Pheromone
beta = 2.0   # Distance
rho = 0.8   # Evaporation rate
Q = 100      # Constant for pheromone deposit
num_ants = 20
num_iterations = 100
initial_pheromone = 0.01

# Euclidean distance function
def distance(P1, P2):
    if P1 == P2:
        return 0.0
    return np.sqrt((P1[0] - P2[0]) ** 2 + (P1[1] - P2[1]) ** 2)

# Total distance
def total_distance(P, seq):
    dist = 0.0
    n = len(seq)
    for i in range(n - 1):
        dist += distance(P[seq[i]], P[seq[i + 1]])
    dist += distance(P[seq[n - 1]], P[seq[0]])  
    return dist

# Read cities from file
def readCities(PNames):
    P = []  # Coordinates of cities
    geolocator = Nominatim(user_agent="VID_GEO_APP")
    with open("./India_cities.txt") as file:
        for line in file:
            city = line.rstrip('\n')
            if not city:
                break
            city += ",India"
            pt = geolocator.geocode(city, timeout=10000)
            y = round(pt.latitude, 2)
            x = round(pt.longitude, 2)
            P.append([x, y])
            PNames.append(city)
    return P

# Plot cities and the path
def plot_cities(seq, P, tot_dist, PNames, iteration=None):
    Pt = [P[seq[i]] for i in range(len(seq))]
    Pt += [P[seq[0]]]
    Pt = np.array(Pt)

    plt.figure()
    title = f'Total Distance: {tot_dist}'
    if iteration is not None:
        title += f' (Iteration {iteration})'
    plt.title(title)
    plt.plot(Pt[:, 0], Pt[:, 1], '-o')

    for i in range(len(P)):
        plt.annotate(PNames[i], (P[i][0], P[i][1]))

    plt.show()

# Choose next city based on pheromone and distance
def choose_next_city(pheromones, distances, visited, current_city):
    probs = []
    for city in range(len(distances)):
        if city not in visited:
            pheromone = pheromones[current_city][city] ** alpha
            heuristic = (1.0 / distances[current_city][city]) ** beta
            probs.append(pheromone * heuristic)
        else:
            probs.append(0)
    probs = np.array(probs) / np.sum(probs)
    return np.random.choice(range(len(distances)), p=probs)

# Ant Colony Optimization algorithm
def ant_colony_optimization(cities, PNames, num_ants, num_iterations):
    num_cities = len(cities)
    
    #pheromone matrix
    pheromones = np.full((num_cities, num_cities), initial_pheromone)
    distances = np.array([[distance(cities[i], cities[j]) for j in range(num_cities)] for i in range(num_cities)])

    best_tour = None
    best_tour_length = float('inf')

    for iteration in range(num_iterations):
        all_tours = []
        all_lengths = []

        for ant in range(num_ants):
            current_city = 0  # Start from city 0
            tour = [current_city]
            visited = set(tour)

            for _ in range(num_cities - 1):
                next_city = choose_next_city(pheromones, distances, visited, current_city)
                tour.append(next_city)
                visited.add(next_city)
                current_city = next_city

            tour_length = total_distance(cities, tour)
            all_tours.append(tour)
            all_lengths.append(tour_length)

            if tour_length < best_tour_length:
                best_tour_length = tour_length
                best_tour = tour

        # Evaporate pheromones
        pheromones *= (1 - rho)

        # Update pheromones
        for tour, length in zip(all_tours, all_lengths):
            pheromone_deposit = Q / length
            for i in range(num_cities - 1):
                pheromones[tour[i]][tour[i + 1]] += pheromone_deposit
            pheromones[tour[-1]][tour[0]] += pheromone_deposit  # Return to start

        # Print iteration info
        print(f"Iteration {iteration + 1}: Best tour length: {best_tour_length}")

        # Plot intermediate result every 20 iterations
        if (iteration + 1) % 20 == 0 or iteration == num_iterations - 1:
            plot_cities(best_tour, cities, best_tour_length, PNames, iteration + 1)

        # stop early if no significant improvement
        if iteration > 10 and np.std(all_lengths) < 1e-2:
            break

    return best_tour, best_tour_length


if __name__ == "__main__":
    PNames = []
    P = readCities(PNames)  
    num_of_cities = len(P)

    # ACO
    best_tour, best_tour_length = ant_colony_optimization(P, PNames, num_ants, num_iterations)
    print("Best Tour Length:", best_tour_length)

    # Final plot of the best result
    plot_cities(best_tour, P, best_tour_length, PNames)
