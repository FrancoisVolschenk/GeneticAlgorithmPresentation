from Blob import Blob
from math import atan2, sin, cos, hypot, pi, fabs
import numpy as np

MAX_SPEED = 1.0
MAX_ENERGY = 100.0
MAX_VISION_DISTANCE = 500.0
MAX_EAT_DISTANCE = 15


def wrap_angle(angle):
    """Keep the angles that the agent is exposed to between -pi and pi"""
    return (angle + pi) % (2 * pi) - pi


def mutate(genome, mutation_rate=0.01, mutation_strength=0.1):
    """Pick random points in the genome and alter their value a little bit"""
    for i in range(len(genome)):
        if np.random.rand() < mutation_rate:
            genome[i] += np.random.normal(0, mutation_strength)
    return genome


class Brain:
    """A simple neural network represented by a matrix of weights for the connections between neurons"""

    def __init__(self, input_size, hidden_size, n_hidden, output_size):
        # The neural network is initiated with random weights in the graph
        self.input_weights = np.random.randn(hidden_size, input_size)
        self.input_biases = np.random.randn(hidden_size, 1)

        self.hidden_layers = []
        self.hidden_biases = []
        for _ in range(n_hidden - 1):
            self.hidden_layers.append(np.random.randn(hidden_size, hidden_size))
            self.hidden_biases.append(np.random.randn(hidden_size, 1))

        self.output_weights = np.random.randn(output_size, hidden_size)
        self.output_biases = np.random.randn(output_size, 1)

    def forward(self, input_vec):
        """This method performs the forward pass through the neural net. At each layer,
        I use tanh as the activation function"""
        x = np.array(input_vec).reshape(-1, 1)

        # Pass through the input layer
        x = np.tanh(self.input_weights @ x + self.input_biases)

        # Pass through the hidden layers
        for W, B in zip(self.hidden_layers, self.hidden_biases):
            x = np.tanh(W @ x + B)

        # Output layer
        output = self.output_weights @ x + self.output_biases
        return output

    def to_genome(self):
        """This method condenses the network into a 1D array of values, to make crossover easier"""
        genome = []
        genome.extend(self.input_weights.flatten())
        genome.extend(self.input_biases.flatten())
        for W, B in zip(self.hidden_layers, self.hidden_biases):
            genome.extend(W.flatten())
            genome.extend(B.flatten())
        genome.extend(self.output_weights.flatten())
        genome.extend(self.output_biases.flatten())
        return np.array(genome)

    @staticmethod
    def from_genome(genome, input_size, hidden_size, n_hidden, output_size):
        """This allows me to build up a neural network from the genome representation"""
        brain = Brain(input_size, hidden_size, n_hidden, output_size)
        g = genome.copy()

        def pop(n):
            nonlocal g
            val = g[:n]
            g = g[n:]
            return val

        brain.input_weights = pop(hidden_size * input_size).reshape(
            (hidden_size, input_size)
        )
        brain.input_biases = pop(hidden_size).reshape((hidden_size, 1))

        brain.hidden_layers = []
        brain.hidden_biases = []
        for _ in range(n_hidden - 1):
            W = pop(hidden_size * hidden_size).reshape((hidden_size, hidden_size))
            B = pop(hidden_size).reshape((hidden_size, 1))
            brain.hidden_layers.append(W)
            brain.hidden_biases.append(B)

        brain.output_weights = pop(output_size * hidden_size).reshape(
            (output_size, hidden_size)
        )
        brain.output_biases = pop(output_size).reshape((output_size, 1))

        return brain


class NeuralBlob(Blob):
    """This represents the blob that will make use of neural networks to decide its behaviour"""

    def __init__(self, x=0, y=0, width=10, height=10, speed=0.5, bearing=0, brain=None):
        super().__init__(x, y, width, height, speed, bearing)
        self.colour = (0, 255, 0)
        self.brain = (
            Brain(input_size=5, hidden_size=5, n_hidden=2, output_size=2)
            if brain is None
            else Brain.from_genome(
                brain, input_size=5, hidden_size=5, n_hidden=2, output_size=2
            )
        )
        # inputs are speed, energy, distance to food, relative sin, relative cos
        # output is bearing angle, action [speed up, slow down, eat]

    def sense_environment(self, food_list):
        # Normalize speed and energy to be values between 0 and 1
        norm_speed = self.speed / MAX_SPEED
        norm_energy = self.energy / MAX_ENERGY

        # Find nearest food
        nearest_food = None
        min_distance = float("inf")
        for food in food_list:
            dx = food.x - self.x
            dy = food.y - self.y
            dist = hypot(dx, dy)
            if dist < min_distance:
                min_distance = dist
                nearest_food = food

        # If no food found, default to max distance and angle = 0
        if nearest_food is None:
            norm_dist = 1.0
            sin_theta = 0.0
            cos_theta = 1.0
        else:
            # Distance should be a value between 0 and 1 as well
            norm_dist = min(min_distance / MAX_VISION_DISTANCE, 1.0)

            # Get relative angle to food
            angle_to_food = atan2(nearest_food.y - self.y, nearest_food.x - self.x)
            relative_angle = wrap_angle(angle_to_food - self.bearing)

            # Break down the angle components to that food
            sin_theta = sin(relative_angle)
            cos_theta = cos(relative_angle)

        return [norm_speed, norm_energy, norm_dist, sin_theta, cos_theta]

    def try_eat(self, food_items):
        self.energy -= 1  # It takes energy to eat, so dont just spam that move
        nearest_food = None
        min_distance = float("inf")
        for food in food_items:
            dx = food.x - self.x
            dy = food.y - self.y
            dist = hypot(dx, dy)
            if dist < min_distance:
                min_distance = dist
                nearest_food = food

        if nearest_food is not None and min_distance <= MAX_EAT_DISTANCE:
            nearest_food.eat()
            self.energy += min(100, self.energy + 50)
            self.score += 3

    def decide_move(self, food_items):
        # Pass the inputs through the brain and decide how to act
        bearing_delta, action = self.brain.forward(self.sense_environment(food_items))
        MAX_TURN = pi / 8
        self.bearing += bearing_delta * MAX_TURN
        self.bearing = wrap_angle(self.bearing)
        dx = self.speed * cos(self.bearing)
        dy = self.speed * sin(self.bearing)
        self.x += dx
        self.y += dy
        self.energy -= self.speed + 0.01
        if self.energy <= 0:
            self.colour = (10, 10, 10)
            self.dead = True

        action = (action + 1) / 2
        if action < 0.33:
            self.speed = min(1.0, self.speed + 0.05)  # speed up
        elif action < 0.66:
            self.speed = max(0.1, self.speed - 0.05)  # slow down
        else:
            self.try_eat(food_items)

        # Use the green intensity to show how much energy the blob has left
        green = min(fabs(int((self.energy / 100) * 255)), 255)
        self.colour = (0, green, 0)

    def crossover(self, other):
        """This uses one point crossover to generate offspring from two blobs"""
        brain1 = self.brain.to_genome()
        brain2 = other.brain.to_genome()
        new_brain1 = np.append(brain1[0 : len(brain1) // 2], brain2[len(brain2) // 2 :])
        new_brain2 = np.append(brain2[0 : len(brain2) // 2], brain1[len(brain1) // 2 :])

        return mutate(new_brain1), mutate(new_brain2)
