import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
import threading
import time
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# === CONFIG ===
IMAGE_PATH = "3 - ImageEvolver/img1.png"  # path to target image
POP_SIZE = 100
BASE_MUTATION_MAX = 0.7
BASE_MUTATION_MIN = 0.01
MUTATION_DECAY_ALPHA = 2.0
GENERATIONS = 10000
ELITE_COUNT = 10
SUCCESS_THRESHOLD = -5

target_img = Image.open(IMAGE_PATH).convert("L").resize(((256, 128)))
target_array = np.array(target_img, dtype=np.uint8).flatten()


def fitness(individual):
    # We calculate a negative distance measure, so we want to maximise the value
    diff = individual.astype(np.int32) - target_array.astype(np.int32)
    score = -np.mean(np.abs(diff))
    return score


def mutate(individual, mutation_rate, max_delta=30):
    mutant = individual.copy()
    num_mutations = int(len(mutant) * mutation_rate)
    if num_mutations == 0:
        return mutant

    indices = np.random.choice(len(mutant), num_mutations, replace=False)

    deltas = np.random.randint(-max_delta, max_delta + 1, num_mutations)

    mutant[indices] = np.clip(mutant[indices] + deltas, 0, 255)

    return mutant


def crossover(parent1, parent2):
    # 1pt crossover
    mask = np.random.rand(len(parent1)) > 0.5
    child = np.where(mask, parent1, parent2)
    return child


def evolve(population, best_fitness_so_far):
    scores = np.array([fitness(individual) for individual in population])
    ranked = np.argsort(scores)[::-1]
    best_idx = ranked[0]
    best_score = scores[best_idx]

    # The top 20% of individuals are selected for reproduction
    retain_length = max(2, POP_SIZE // 5)
    parents = [population[i] for i in ranked[:retain_length]]
    parent_scores = scores[ranked[:retain_length]]

    # We want to keep at least a few good solutions intact
    elite_count = min(ELITE_COUNT, POP_SIZE)
    elites = [population[i] for i in ranked[:elite_count]]

    # Proportional selection
    fitness_exp = np.exp(parent_scores - np.max(parent_scores))
    selection_probs = fitness_exp / (fitness_exp.sum() + 1e-8)

    # We adapt the mutatino rate based on how well the best individual is doing
    if best_fitness_so_far == float("-inf"):
        norm_progress = 0.0
    else:
        norm_progress = np.clip(
            1.0 - abs(best_score) / 255.0, 0.0, 1.0
        )  # Normalise the best fitness score in a range of [0, 1)

    # Smooth nonlinear decay from BASE_MUTATION_MAX → BASE_MUTATION_MIN
    mutation_rate = BASE_MUTATION_MIN + (
        BASE_MUTATION_MAX - BASE_MUTATION_MIN
    ) * np.exp(-MUTATION_DECAY_ALPHA * norm_progress)
    mutation_rate = float(np.clip(mutation_rate, BASE_MUTATION_MIN, BASE_MUTATION_MAX))

    # Make at least two children from the top individuals
    top_parents = parents[:2]
    children = []
    for _ in range(ELITE_COUNT):
        p1, p2 = random.choices(top_parents, k=2)
        child = crossover(p1, p2)
        child = mutate(child, mutation_rate)
        children.append(child)

    while len(children) + elite_count < POP_SIZE:
        p1, p2 = random.choices(parents, weights=selection_probs, k=2)
        child = crossover(p1, p2)
        child = mutate(child, mutation_rate)
        children.append(child)

    new_population = np.array(elites + children, dtype=np.uint8)
    return new_population, population[best_idx], best_score, mutation_rate


# === UI SETUP ===
root = tk.Tk()
root.title("Genetic Image Evolution")

display_frame = tk.Frame(root)
display_frame.pack(padx=10, pady=10)

plot_frame = tk.Frame(root)
plot_frame.pack(padx=10, pady=10)

img_label = tk.Label(display_frame)
img_label.pack()

status = tk.Label(display_frame, text="Starting evolution...")
status.pack()

fig = Figure(figsize=(4, 3), dpi=100)
ax = fig.add_subplot(111)
ax.set_title("Fitness over Generations")
ax.set_xlabel("Generation")
ax.set_ylabel("Best Fitness")
ax.grid(True)

canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.draw()
canvas.get_tk_widget().pack()

fitness_history = []


def run_evolution():
    population = np.random.randint(
        0, 256, (POP_SIZE, len(target_array)), dtype=np.uint8
    )
    best_score = float("-inf")
    best = None
    run = True

    gen = 0
    while run:
        population, best_candidate, score, mutation_rate = evolve(
            population, best_score
        )
        fitness_history.append(score)

        if score > best_score:
            best_score = score
            best = best_candidate

        if gen % 10 == 0:
            img = Image.fromarray(
                best.reshape(target_img.size[::-1]).astype(np.uint8), mode="L"
            )
            tk_img = ImageTk.PhotoImage(img)

            def update_ui():
                img_label.configure(image=tk_img)
                img_label.image = tk_img
                status.config(
                    text=f"Gen {gen} | Fitness: {score:.3f} | Mutation: {mutation_rate:.4f}"
                )

                ax.clear()
                ax.set_title("Fitness per generation")
                ax.set_xlabel("Generation")
                ax.grid(True)
                ax.plot(fitness_history, label="Best Fitness", color="red")
                canvas.draw_idle()

            root.after(0, update_ui)
        if score >= SUCCESS_THRESHOLD:
            run = False

        gen += 1

    status.config(text=f"Done! Best fitness: {best_score:.0f}")


threading.Thread(target=run_evolution, daemon=True).start()

root.mainloop()
