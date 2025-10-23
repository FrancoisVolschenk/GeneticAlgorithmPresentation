import numpy as np
import random

items = [
    {"name": "Tent", "weight": 5.0, "value": 10},
    {"name": "Sleeping Bag", "weight": 3.0, "value": 8},
    {"name": "Cooking Pot", "weight": 2.0, "value": 5},
    {"name": "Gas Stove", "weight": 1.5, "value": 6},
    {"name": "Water Bottle", "weight": 1.0, "value": 4},
    {"name": "Food Supplies", "weight": 4.0, "value": 9},
    {"name": "First Aid Kit", "weight": 1.0, "value": 7},
    {"name": "Flashlight", "weight": 0.5, "value": 3},
    {"name": "Map & Compass", "weight": 0.3, "value": 5},
    {"name": "Extra Clothes", "weight": 2.5, "value": 6},
    {"name": "Hiking Boots", "weight": 2.2, "value": 8},
    {"name": "Rain Jacket", "weight": 1.2, "value": 6},
    {"name": "Portable Charger", "weight": 0.4, "value": 4},
    {"name": "Camera", "weight": 0.8, "value": 5},
    {"name": "Hat & Gloves", "weight": 0.6, "value": 3},
    {"name": "Rope", "weight": 1.8, "value": 6},
    {"name": "Multi-tool", "weight": 0.7, "value": 7},
    {"name": "Trekking Poles", "weight": 1.1, "value": 5},
    {"name": "Notebook & Pen", "weight": 0.5, "value": 2},
    {"name": "Book / Entertainment", "weight": 0.7, "value": 3},
]

WEIGHT_LIMIT = 20

POP_SIZE = 40
GENERATIONS = 150
MUTATION_RATE = 0.05
ELITE_SIZE = 2


def fitness(individual):
    total_weight = np.sum(
        [item["weight"] * gene for item, gene in zip(items, individual)]
    )

    total_value = np.sum(
        [item["value"] * gene for item, gene in zip(items, individual)]
    )

    if total_weight > WEIGHT_LIMIT:
        return 0  # Eliminate overweight solutions
    return total_value


def initialize_population(size, num_items):
    return [np.random.randint(0, 2, num_items) for _ in range(size)]


def roulette_wheel_selection(population):
    fitness_values = np.array([fitness(individual) for individual in population])
    total_fit = np.sum(fitness_values)

    if total_fit == 0:
        return random.choice(population)

    pick = random.uniform(0, total_fit)
    current = 0

    for individual, fit in zip(population, fitness_values):
        current += fit
        if current >= pick:
            return individual

    return population[-1]


def two_point_crossover(parent1, parent2):
    length = len(parent1)

    if length < 2:
        return parent1.copy(), parent2.copy()

    points = sorted(random.sample(range(1, length - 1), 2))
    c1, c2 = parent1.copy(), parent2.copy()

    c1[points[0] : points[1]] = parent2[points[0] : points[1]]
    c2[points[0] : points[1]] = parent1[points[0] : points[1]]

    return c1, c2


def mutate(individual):
    mutant = individual.copy()

    for i in range(len(mutant)):
        if random.random() < MUTATION_RATE:
            mutant[i] = 1 - mutant[i]

    return mutant


def genetic_algorithm():
    population = initialize_population(POP_SIZE, len(items))
    best_solution = None
    fitness_history = []

    for gen in range(GENERATIONS):
        population.sort(key=lambda individual: fitness(individual), reverse=True)
        best_solution = population[0]
        best_fit = fitness(best_solution)
        fitness_history.append(best_fit)

        print(f"Gen {gen:3d} | Best Fitness: {best_fit:3d}")

        # Elitism
        new_population = population[:ELITE_SIZE]

        # Generate offspring
        while len(new_population) < POP_SIZE:
            parent1 = roulette_wheel_selection(population)
            parent2 = roulette_wheel_selection(population)

            child1, child2 = two_point_crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)

            new_population.extend([child1, child2])

        population = new_population[:POP_SIZE]

    # Final result
    print("\n Best packing plan found:")
    total_weight = np.sum([item["weight"] * g for item, g in zip(items, best_solution)])
    total_value = np.sum([item["value"] * g for item, g in zip(items, best_solution)])
    for item, g in zip(items, best_solution):
        if g == 1:
            print(
                f"  - {item['name']} (weight: {item['weight']} kg, value: {item['value']})"
            )

    print(f"\nTotal weight: {total_weight:.1f} kg")
    print(f"Total value: {total_value}")

    return fitness_history


if __name__ == "__main__":
    history = genetic_algorithm()
