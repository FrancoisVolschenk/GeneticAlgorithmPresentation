import pygame
from NeuralBlob import NeuralBlob
from Food import Food
import random


# World set up
WORLD_WIDTH = 800
WORLD_HEIGHT = 800
TOP_N_SURVIVE = 5
POPULATION_SIZE = 30
NUM_FOOD = 100

# Visualisation setup
pygame.init()
screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
clock = pygame.time.Clock()
running = True
blobs = []
food = []


def spawn_food():
    global food
    food = []
    for f in range(NUM_FOOD):
        food.append(Food(WORLD_WIDTH, WORLD_HEIGHT))


# No selection and crossover in the first generation
def start_generation():
    for blob in range(POPULATION_SIZE):
        blobs.append(
            NeuralBlob(
                x=random.randint(0, WORLD_WIDTH),
                y=random.randint(0, WORLD_HEIGHT),
                speed=1,
            )
        )


# All subsequent generations need selection and crossover
def next_generation():
    global blobs
    blobs.sort(key=lambda x: x.score, reverse=True)
    top = blobs[:TOP_N_SURVIVE]
    blobs = []
    # Make offspring from the top performers
    for i in range(TOP_N_SURVIVE - 1):
        brain1, brain2 = top[i].crossover(top[i + 1])
        child1 = NeuralBlob(
            x=random.randint(0, WORLD_WIDTH),
            y=random.randint(0, WORLD_HEIGHT),
            speed=1,
            brain=brain1,
        )
        child2 = NeuralBlob(
            x=random.randint(0, WORLD_WIDTH),
            y=random.randint(0, WORLD_HEIGHT),
            speed=1,
            brain=brain2,
        )
        blobs += [child1, child2]

    # Fill the rest of the spots with new randomly initialised blobs
    while len(blobs) < POPULATION_SIZE:
        blobs.append(NeuralBlob(x=250, y=250, speed=1))


def draw_objects(objects):
    for obj in objects:
        pygame.draw.rect(screen, obj.colour, (obj.x, obj.y, obj.width, obj.height))


def draw_food(food_list):
    for food in food_list:
        pygame.draw.circle(screen, food.colour, (food.x, food.y), food.radius)


def move_blobs():
    for blob in blobs:
        if not blob.dead:
            blob.decide_move(food)


def all_dead():
    for blob in blobs:
        if not blob.dead:
            return False
    return True


spawn_food()
start_generation()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if all_dead():
        print("End of generation. Starting new one")
        spawn_food()
        next_generation()

    screen.fill("black")
    move_blobs()
    draw_objects(blobs)
    draw_food(food)

    pygame.display.update()
    clock.tick(60)
pygame.quit()

### TODO: Complete QBlobs, set up adersarial simulation between QBlobs and NearalBlobs
### Maybe introduce some predators or predatory behaviour under one of the groups of blobs
