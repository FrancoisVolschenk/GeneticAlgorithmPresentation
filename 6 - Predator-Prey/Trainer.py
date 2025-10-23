from tkinter import Text, END

import World
import random
import Visualizer
import pickle

# Pseudo Infinity for the purposes of finding an arbitrary maximum value without a proper starting value
ARB_MAX = 1000000000000

class GeneticAlgorithm:
    """This class represents the methods of the genetic algorithm"""
    def __init__(self, popSize, numGenerations, numSurvivors, threshold, mutationRate):
        self.popSize = popSize
        self.numGenerations = numGenerations
        if numSurvivors > popSize:
            self.numSurvivors = popSize
        else:
            self.numSurvivors = numSurvivors
        if mutationRate < 0 or mutationRate > 1.0:
            mutationRate = 0.5
        self.threshold = threshold
        self.mutationRate = mutationRate

    def mutate(self, brain):
        # This method is used to introduce mutations to the weights and biases of the population
        numLayers = len(brain)
        for l in range(numLayers):
            weights = brain[l][0]
            biases = brain[l][1]

            for b in range(len(biases)):
                if random.random ()> self.mutationRate:
                    bias = random.randint(0, 100) / 100
                    biases[b] = bias

            for input in range(len(weights)):
                for output in range(len(weights[input])):
                    if random.random() > self.mutationRate:
                        weights[input][output] += random.randint(0, 100) / 100

    def crossover(self, brain1, brain2):
        # This method is used to mix the genes of the top performers to create agents in the new generation
        parent1 = brain1[1]
        parent2 = brain2[1]

        numLayers = len(parent1)
        newBrain = []
        for l in range(numLayers):
            p1Weights = parent1[l][0]
            p1Biases = parent2[l][1]
            p2Weights = parent2[l][0]
            p2Biases = parent2[l][1]

            # there is a 50/50 chance to take a weight gene from either parent
            newWeight = []
            for w in range(len(p1Weights)):
                if random.randint(0, 100) % 2 == 0:
                    newWeight.append(p1Weights[w])
                else:
                    newWeight.append(p2Weights[w])

            # there is a 50/50 chance to take a bias gene from each parent
            newBias = []
            for b in range(len(p1Biases)):
                if random.randint(0, 100) % 2 == 0:
                    newBias.append(p1Biases[b])
                else:
                    newBias.append(p2Biases[b])

            newBrain.append((newWeight, newBias))

        # introduce variety into the population
        self.mutate(newBrain)
        return newBrain

    def createNewGen(self, lstPopulationData):
        # This method uses the existing population to create a new population
        lstNewGen = []

        # save some of the fittest members of the previous population
        for k in range(self.numSurvivors):
            lstNewGen.append(World.Player())
            self.mutate(lstPopulationData[k][1])
            lstNewGen[k].setBrain(lstPopulationData[k][1])

        # fill the rest of the remaining population space with new candidates created by breeding the members of the previous population
        popIndex = 0
        while len(lstNewGen) < self.popSize:
            newAgent = World.Player()
            newAgent.setBrain(self.crossover(lstPopulationData[popIndex], lstPopulationData[popIndex + 1]))
            popIndex += 1
            lstNewGen.append(newAgent)
        return lstNewGen

    def saveAgent(self, agent: World.Player, identifier: float):
        # save the configuration of an agent to a file
        with open(f"Agents/agent{identifier}.ai", "wb") as file:
                pickle.dump(agent, file)

    def train(self, show: bool, world: World.Environment, output: Text = None):
        """This method runs the genetic algorithm using the given parameters"""

        vis = None
        bSaved = False
        # Visualization of the training is optional
        if show:
            vis = Visualizer.Vis(world)

        # Keep track of the current population's agents
        lstPlayers = []
        # This loop generates the first generation
        for p in range(self.popSize):
            lstPlayers.append(World.Player())

        bestAgent = None
        bestScore = -ARB_MAX
        thresholdReached = False

        # Iterate over the number of generations
        gens = 0
        #for gens in range(self.numGenerations):
        while gens != self.numGenerations:
            lstPlayerData = [] # This list will keep track of how well each agent has performed before dying
            for agent in range(len(lstPlayers)): # loop over each agent in the current generation
                world.setPlayer(lstPlayers[agent])
                data = world.tick() # move the agent in the world
                if show:
                    data = vis.runSimulation(gens, agent)
                else:
                    while data is None: # continue until the move function returns a brain (meaning the agent has died)
                        data = world.tick()
                if world.player.numEats >= self.threshold:
                    thresholdReached = True
                    if output is None:
                        print(f"found a winner!. Saving to file agent{agent}")
                    else:
                        output.insert(END, f"found a winner!. Saving to file agent{agent}\n")
                    self.saveAgent(lstPlayers[agent], agent)
                    bSaved = True
                lstPlayerData.append(data) # store that data in the list

            lstPlayerData.sort(key = lambda p: p[0]) # sort the agents by their score (fitness function)
            lstPlayerData.reverse() # reverse the order so that the best performers are at the top of the list

            if lstPlayerData[0][0] > bestScore:
                bestScore = lstPlayerData[0][0]
                bestAgent = lstPlayerData[0][1]

            if output is None:
                print(f"generation {gens}    Best Score: {lstPlayerData[0][0]}")
            else:
                output.insert(END, f"generation {gens}; Best: {lstPlayerData[0][0]}\n")

            if thresholdReached:
                break
            
            lstPlayers = self.createNewGen(lstPlayerData)
            gens += 1 

        if not bSaved:
            toSave = World.Player()
            toSave.setBrain(bestAgent)
            self.saveAgent(toSave, -3.14)

        if vis is not None:
            vis.done()

if __name__ == "__main__":
    # if the trainer is run by itself, it provides a command line interface to initiate the training
    width = int(input("How many columns should there be in the world?:\n"))
    height = int(input("How many rows should there be in the world?:\n"))
    world = World.Environment(width, height)
    if input("Would you like to train from scratch? (y/n):\n") == "y":    
        numPerGeneration = int(input("how many players do you wish to have per generation?\n"))
        numKeepers = int(input("How many top performers do you wish to carry over?\n"))
        numGenerations = int(input("How many generations do you wish to train?\n"))
        threshold = int(input("What number of consecutive eats would count as a win?\n"))
        mutationRate = float(input("Please enter a mutation rate (0.0 - 1.0):\n"))
        show = (input("Would you like to visualize the training? (y/n): \n")) == "y"
        ga = GeneticAlgorithm(numPerGeneration, numGenerations, numKeepers, threshold, mutationRate)
        ga.train(show, world)
    else:
        agentFl = input("please enter the name of the agent file you wish to load:\n")
        with open("Agents/" + agentFl, "rb") as file:
            agent = pickle.load(file)
        agent.pos = [1, 1]
        agent.score = 0
        agent.energy = 50
        world.setPlayer(agent)
        vis = Visualizer.Vis(world)
        data = vis.runSimulation(0, 0)

def TrainFromScratch(width: int, height: int, numPerGen: int, numKeepers: int, numGens: int, threshold: int, mutationRate: float, show: bool, output: Text = None):
    world = World.Environment(width, height)
    ga = GeneticAlgorithm(numPerGen, numGens, numKeepers, threshold, mutationRate)
    ga.train(show, world, output)

def simulate(width: int, height: int, agentFile: str):
    world = World.Environment(width, height)
    with open("Agents/" + agentFile, "rb") as file:
        agent = pickle.load(file)

    agent.pos = [1, 1]
    agent.score = 0
    agent.energy = 50
    agent.numEats = 0
    world.setPlayer(agent)
    vis = Visualizer.Vis(world)
    data = vis.runSimulation(0, 0)
    vis.done()

