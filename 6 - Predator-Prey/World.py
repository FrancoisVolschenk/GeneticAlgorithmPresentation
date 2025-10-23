import Brain
import random
import math

def calcDist(p1, p2):
        # Calculate the Euclidean distance between two given positions
        return math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow(p1[1] - p2[1], 2))
        # return (math.fabs(p1[0] - p2[0]) + math.fabs(p1[1] - p2[1]))

class Obstacle:
    """This class represents the obstacles that hinder the agent and the predator"""
    def __init__(self, pos):
        self.pos = pos

class Predator:
    """This class represents the predator. A reflex agent that consistently follows the prey"""
    def __init__(self):
        self.pos = [0, 0]
        self.speed = 0.5
        self.stuck = False

    def move(self, target):
        # Given a target position (prey location), move towards that location
        actions = []
        x, y = self.pos

        # Build a list of potential actions
        if target[1] < y:
            actions.append(0)
        if target[1] > y:
            actions.append(1)
        if target[0] < x:
            actions.append(2)
        if target[0] > x:
            actions.append(3)
        actions.append(4) # do nothing

        # Select a random action from the list
        choice = random.choice(actions)
        if choice == 0:
            y -= self.speed
        if choice == 1:
            y += self.speed
        if choice == 2:
            x -= self.speed
        if choice == 3:
            x += self.speed

        # Attempt to adjust the speed of the predator based on its distance from the prey
        # distance = calcDist(self.pos, target)
        # if distance < 2:
        #     self.speed = 0.2
        # if distance > 4:
        #     self.speed = 0.5 

        # update predator position based on selected action
        self.pos = [x, y]

class Player:
    """This class represents the prey.
      An intelligent agent that makes use of a neural network to decide the best action to avoid the predator 
      and find food"""
    def __init__(self):
        self.pos = [0, 0]
        self.score = 0
        self.energy = 50
        self.numEats = 0

        # The lists represent the number of inputs to, and outputs from each layer in the network
        layers = [[8, 4]]
        self.brain = Brain.NeuralNetwork(layers)

        # initialize choice to a void option
        self.choice = -1
        self.currentFoodDist = 0
        self.currentPredDist = 0
        self.stuck = False

    def setBrain(self, newBrain):
        # Use this to assign a network that was generated externally
        self.brain.setBrain(newBrain)

    def senseFood(self, food_pos):
        # Determine which direction the food item is
        food_x, food_y = food_pos
        currentX, currentY = self.pos
        lstResult = []

        # Determine the boolean representation to "is there food in this direction?"
        lstResult.append(1 if currentY > food_y else 0) # up
        lstResult.append(1 if currentY < food_y else 0) # down
        lstResult.append(1 if currentX > food_x else 0) # left
        lstResult.append(1 if currentX < food_x else 0) # right

        return lstResult
    
    def senseDanger(self, pred_pos, obstacles, world_width, world_height):
        # Determine if there is danger in the form of the predator, world edges, or obstacles in each direction
        pred_x, pred_y = pred_pos
        currentX, currentY = self.pos
        lstResults = []

        # Calculate the distances to each of the potential sources of danger
        predDist = calcDist(self.pos, pred_pos)
        topDist = calcDist(self.pos, [currentX, 0])
        bottomDist = calcDist(self.pos, [currentX, world_height])
        leftDist = calcDist(self.pos, [0, currentY])
        rightDist = calcDist(self.pos, [0, world_width])

        # determine if the closest object poses a threat in any of the directions
        closestObstacle = obstacles[0]
        closestObDist = calcDist(self.pos, obstacles[0].pos)
        for o in obstacles:
            dist = calcDist(self.pos, o.pos)
            if dist < closestObDist:
                closestObstacle = o
                closestObDist = dist

        obX, obY = closestObstacle.pos

        # Determine the boolean representation of "is there danger in this direction?"
        # lstResults.append(1 if ((currentY <  pred_y and currentX == pred_x) and (predDist <= 2)) or ((currentY <  obY and currentX == obX) and (closestObDist <= 1)) or (bottomDist <= 1) else 0) # Danger Down
        # lstResults.append(1 if ((currentY >  pred_y and currentX == pred_x) and (predDist <= 2)) or ((currentY >  obY and currentX == obX) and (closestObDist <= 1)) or (topDist <= 1) else 0) # Danger Up
        # lstResults.append(1 if ((currentY == pred_y and currentX <  pred_x) and (predDist <= 2)) or ((currentY ==  obY and currentX < obX) and (closestObDist <= 1)) or (rightDist <= 1) else 0) # Danger Right
        # lstResults.append(1 if ((currentY == pred_y and currentX >  pred_x) and (predDist <= 2)) or ((currentY ==  obY and currentX > obX) and (closestObDist <= 1)) or (leftDist <= 1) else 0) # Danger Left        
        lstResults.append(1 if ((currentY <  pred_y and currentX == pred_x) and (predDist <= 2))else 0)
        lstResults.append(1 if ((currentY >  pred_y and currentX == pred_x) and (predDist <= 2)) else 0)
        lstResults.append(1 if ((currentY == pred_y and currentX <  pred_x) and (predDist <= 2)) else 0)
        lstResults.append(1 if ((currentY == pred_y and currentX >  pred_x) and (predDist <= 2)) else 0)



        return lstResults

    def move(self, food_pos, pred_pos, obstacles, world_width, world_height):
        # Determine which direction to move into based on what the agent can sense
        targetX, targetY = self.pos
        lstInputs = []

        # keep track of how far the agent is from food to determine if it moved any closer
        self.currentFoodDist = calcDist(self.pos, food_pos)
        self.currentPredDist = calcDist(self.pos, pred_pos)

        # sense the world around the agent
        lstInputs += self.senseFood(food_pos) 
        self.senseDanger(pred_pos, obstacles, world_width, world_height)  
        lstInputs += self.senseDanger(pred_pos, obstacles, world_width, world_height)   

        # determine which action to take
        self.choice = self.brain.decideAction(lstInputs)

        if self.choice == 0: # up
            targetY -= 1
        elif self.choice == 1: # down
            targetY += 1
        elif self.choice == 2: # left
            targetX -= 1
        elif self.choice == 3: # right
            targetX += 1

        # Update the agent's position and decrease the agent's energy
        self.pos = [targetX, targetY]
        self.energy -= 1
    
    def evaluateAction(self, food_pos, pred_pos):
        # Determine if the action that was taken got the agent in a better position or not
        newFoodDist = calcDist(self.pos, food_pos)
        newPredDist = calcDist(self.pos, pred_pos)
        if newFoodDist < self.currentFoodDist:
            self.score += 1
        else:
            self.score -= 2

        if newPredDist <= 4:
            self.score -= 5
        # if newPredDist > self.currentPredDist:
        #     self.score += 1
        # else:
        #     self.score -= 4

        self.currentFoodDist = newFoodDist
        self.currentPredDist = newPredDist
    
class Food:
    """This class represents the food that the agent must collect to survive.
        For experimentation purposes, the food also has the ability to move."""
    def __init__(self):
        self.pos = [0, 0]

    def respwan(self, pos):
        # replace the food in the world when it has been eaten
        self.pos = pos

    def move(self, wl, hl):
        # Move in a random direction
        tx, ty = self.pos
        rx = random.randint(0, 100)
        ry = random.randint(0, 100)
        if rx <= 50:
            tx += 1
        if rx > 50:
            tx -= 1
        if ry <= 50:
            ty += 1
        if ry > 50:
            ty -= 1
        if tx >= 1 and tx < wl:
            self.pos[0] = tx
        if ty >= 1 and ty < hl:
            self.pos[1] = ty

class Environment:
    """This class represents the world that the simulation takes place in
        It has obstacles set up at random, but they do not move after begin set up.
        Food is placed randomly and only moves if the player collects it."""
    def __init__(self, width: int, height: int):
        self.world_width = width
        self.world_height = height

        self.actions = ["up", "down", "left", "right"]
        self.player = None
        self.food = Food()
        self.predator = Predator()

        self.spawnFood()
        self.spawnPredator()
        self.lstObstacles = []
        self.placeObstacles(5)

    def setPlayer(self, player: Player):
        # if an agent was loaded from an external file, it is not generated by the world
        self.player = player
        self.player.pos = self.placeRandom()

    def isInWorld(self, pos):
        # determine if a certain position is inside of the bounds of the world
        return not ((pos[0] <= 1 or pos[0] >= self.world_width - 1) or (pos[1] <= 1 or pos[1] >= self.world_height - 1))

    def placeRandom(self):
        # Generate a random position that exist within the world and is at least one position from the wall
        x = random.randint(2, self.world_width - 2)
        y = random.randint(2, self.world_height - 2)
        return [x, y]

    def spawnFood(self):
        # Relocate the food
        self.food.respwan(self.placeRandom())
    
    def spawnPredator(self):
        # randomly place the predator
        self.predator.pos = self.placeRandom()

    def spawnPlayer(self):
        # randomly place the player
        self.player.pos = self.placeRandom()

    def placeObstacles(self, numObstacles):
        # place the obstacles at random positions
        for o in range(numObstacles):
            self.lstObstacles.append(Obstacle(self.placeRandom()))

    def tick(self):
        """Evolve the state of the world"""

        # if the player is not currently stuck, they can move, and have a chance to get stuck
        if not self.player.stuck:
            self.player.move(self.food.pos, self.predator.pos, self.lstObstacles, self.world_width, self.world_height)
            for o in self.lstObstacles:
                if self.player.pos == o.pos:
                    self.player.stuck = True
                    break
        else:
            # if the agent is stuck, they have a chance to get unstuck
            if random.randint(0, 100) % 5 == 0:
                self.player.stuck = False
        
        # if the predator is not stuck, it can move and has a chance of getting stuck
        if not self.predator.stuck:
            self.predator.move(self.player.pos)
            for o in self.lstObstacles:
                if self.predator.pos == o.pos:
                    self.predator.stuck = True
                    break
        else:
            # if the predator is stuck, they have a chance to get unstuck
            if random.randint(0, 100) % 4 == 0:
                self.predator.stuck = False

        inWorld = self.isInWorld(self.player.pos)
        retVal = None

        # Determine if the agent has collected food
        if self.player.pos == self.food.pos:
            self.player.score += 100
            self.player.energy = 50 # restore their energy
            self.player.numEats += 1
            self.spawnFood() # re-place the food

        # Determine if the predator has caught the player
        if  calcDist(self.player.pos, self.predator.pos) <= 0.5:
            self.player.score -= 50
            self.player.energy = 0 # dies

        # determine if the player has moved out of the bounds of the world
        if not inWorld or self.player.energy <= 0:
            brain = self.player.brain.preserveBrain()
            retVal = [self.player.score, brain]
        # self.food.move(self.world_width, self.world_height)

        # Update the fittness of the current agent based on the move it made
        self.player.evaluateAction(self.food.pos, self.predator.pos)
        return retVal # if the agent dies, its brain is preserved to use in the next generation
    