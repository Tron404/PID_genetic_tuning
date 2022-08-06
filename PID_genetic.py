import random
import numpy as np
import signals
from PID_Simulation_no_sliders import pid_loop_update

epochs = 10000
population_size = 2500
target_function = signals.custom_sig

values = np.linspace(0.0, 5.0, num=10000) # values for k_p, k_i
dv = np.linspace(-0.1, 0.1, num=1000) # values for k_d

# how fit an individual is
def fitness_function(signal, target):
    sum = 0
    for sig, tar in zip(signal, target):
        sum += abs(tar-sig)

    return 1/sum

# randomly initialise an individual
def init_individual():
    p = random.choice(values)
    i = random.choice(values)
    d = random.choice(dv)

    return [p, i, d]

# crossover of genes and mutation
def crossover(p1, p2):
    crossover_point = random.randint(0,2)
    mutation = random.random()

    child1 = np.concatenate([p1[:crossover_point], p2[crossover_point:]])
    child2 = np.concatenate([p2[:crossover_point], p1[crossover_point:]])

    if mutation < 0.1:
        gene = random.randint(0,2)
        child_chance = random.random()
        if child_chance < 0.5:
            child1[gene] = random.choice(values)
        else:
            child2[gene] = random.choice(values)

    return child1, child2

population = []
for p in range(population_size):
    population.append(init_individual())

global_max_fitness1, global_max_fitness2 = -1, -1
global_best_individual1, global_best_individual2 = [], []
for e in range(epochs):
    local_max_fitness1, local_max_fitness2 = -1, -1
    local_best_individual1, local_best_individual1 = [], []
    idx_best_individual1, idx_best_individual2 = 0, 0
    for i, p in enumerate(population):
        fitness = fitness_function(pid_loop_update(p, target_function, False), target_function(100))
        if fitness > local_max_fitness1:
            local_max_fitness1 = fitness
            local_best_individual1 = p
            idx_best_individual1 = i
        elif fitness > local_max_fitness2:
            local_max_fitness2 = fitness
            local_best_individual2 = p
            idx_best_individual2 = i

        if fitness > global_max_fitness1:
            global_max_fitness1 = fitness
            global_best_individual1 = p
        elif fitness > global_max_fitness2:
            global_max_fitness2 = fitness
            global_best_individual2 = p

    population[idx_best_individual1], population[idx_best_individual2] = crossover(population[idx_best_individual1], population[idx_best_individual2])

    print(f"Generation {e+1}, in which the two best individuals were {local_best_individual1} and {local_best_individual2}, with fitness {local_max_fitness1} and {local_max_fitness2}")

pid_loop_update(global_best_individual1, target_function, True)
pid_loop_update(global_best_individual2, target_function, True)

print(fitness_function(pid_loop_update(global_best_individual1, target_function, False), target_function(100)))
print(fitness_function(pid_loop_update(global_best_individual2, target_function, False), target_function(100)))
    
    
    

