import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ACO Parameters
num_ants = 20
num_iterations = 50
decay_rate = 0.5
alpha = 1  # Influence of pheromone
beta = 2   # Influence of distance

# Sample cities for TSP problem
cities = np.array([[20, 30], [40, 70], [60, 20], [80, 50], [20, 80], [60, 70], [70, 90], [90, 20]])

# Calculate the distance matrix
num_cities = len(cities)
distances = np.linalg.norm(cities[:, np.newaxis] - cities[np.newaxis, :], axis=2)

# Initialize pheromone matrix with small initial values
pheromones = np.ones((num_cities, num_cities)) * 0.1

# Ant class representing an individual solution
class Ant:
    def __init__(self):
        self.path = []
        self.total_distance = 0

    def visit_city(self, city):
        self.path.append(city)
        if len(self.path) > 1:
            self.total_distance += distances[self.path[-2], self.path[-1]]

    def calculate_distance(self):
        # Complete the tour to the starting city
        self.total_distance += distances[self.path[-1], self.path[0]]
    
    def reset(self):
        self.path = []
        self.total_distance = 0

# ACO Algorithm
class ACO:
    def __init__(self):
        self.ants = [Ant() for _ in range(num_ants)]
        self.best_path = None
        self.best_distance = float('inf')

    def run_iteration(self):
        global pheromones
        for ant in self.ants:
            ant.reset()
            start_city = np.random.randint(num_cities)
            ant.visit_city(start_city)

            # Build the path
            for _ in range(num_cities - 1):
                current_city = ant.path[-1]
                probabilities = self.calculate_transition_probabilities(current_city, ant.path)
                next_city = np.random.choice(range(num_cities), p=probabilities)
                ant.visit_city(next_city)
            ant.calculate_distance()

            # Update best path if found
            if ant.total_distance < self.best_distance:
                self.best_distance = ant.total_distance
                self.best_path = ant.path[:]

        # Update pheromones
        self.update_pheromones()

    def calculate_transition_probabilities(self, current_city, visited):
        pheromone = pheromones[current_city]
        heuristic = 1 / (distances[current_city] + 1e-10)  # Avoid division by zero
        heuristic[visited] = 0  # Don't visit cities already visited
        prob_numerators = (pheromone ** alpha) * (heuristic ** beta)
        return prob_numerators / prob_numerators.sum()

    def update_pheromones(self):
        global pheromones
        pheromones *= (1 - decay_rate)  # Pheromone evaporation
        for ant in self.ants:
            pheromone_contribution = 1 / ant.total_distance
            for i in range(num_cities - 1):
                pheromones[ant.path[i], ant.path[i + 1]] += pheromone_contribution
            # Complete the tour to the starting city
            pheromones[ant.path[-1], ant.path[0]] += pheromone_contribution

# GUI with Tkinter
class ACO_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ant Colony Optimization Visualization")

        # Set up ACO
        self.aco = ACO()
        self.iteration = 0

        # Set up matplotlib figure and canvas
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.scatter(cities[:, 0], cities[:, 1], color='red', s=50, label="Cities")
        self.line, = self.ax.plot([], [], 'b-', label="Best Path")
        self.ax.legend()

        # Create Tkinter Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # Start/Stop Button
        self.run_button = ttk.Button(root, text="Start", command=self.start)
        self.run_button.pack(side=tk.LEFT)

        # Reset Button
        self.reset_button = ttk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT)

        # Track running status and after ID
        self.running = False
        self.after_id = None

    def start(self):
        self.running = not self.running
        self.run_button.config(text="Stop" if self.running else "Start")
        if self.running:
            self.schedule_update()

    def schedule_update(self):
        if self.running:
            self.aco.run_iteration()
            self.update_plot()
            self.iteration += 1
            if self.iteration < num_iterations:
                self.after_id = self.root.after(500, self.schedule_update)
            else:
                self.running = False
                self.run_button.config(text="Start")

    def reset(self):
        self.aco = ACO()
        self.iteration = 0
        self.running = False
        self.run_button.config(text="Start")
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.update_plot()

    def update_plot(self):
        if self.aco.best_path:
            path = self.aco.best_path + [self.aco.best_path[0]]  # Complete the loop
            path_coords = cities[path]
            self.line.set_data(path_coords[:, 0], path_coords[:, 1])
            self.canvas.draw()

# Run the GUI
root = tk.Tk()
app = ACO_GUI(root)
root.mainloop()
