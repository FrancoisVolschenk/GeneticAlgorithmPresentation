import turtle
import World

"""The visualization is loosely coupled from the system, so the training can be done without visualizing it"""
class Vis:
    def __init__(self, world: World.Environment):
        self.world = world
        self.width = self.world.world_width * 20
        self.height = self.world.world_height * 20
        self.screen = None
        self.base_x = (self.width / -2)
        self.base_y = (self.height / 2) - 30

        self.food = None
        self.player = None
        self.predator = None
        self.pen = None
        self.worldExists = False

    def drawWorld(self):
        # Set up the screen
        self.screen = turtle.setup(self.width + 40, self.height + 75)
        draw = turtle.Turtle()
        turtle.Screen().bgcolor("black")
        turtle.Screen().title("AI intelligent prey simulation")

        # Set up the pen to draw borders and obstacles
        draw.speed(0)
        draw.hideturtle()
        draw.penup()
        draw.shape("square")
        draw.color("red")
        draw.seth(0)
        draw.goto(self.base_x, self.base_y)

        # darw the borders
        for b in range(4):
            if b % 2 == 0:
                count = self.world.world_width
            else:
                count = self.world.world_height
            for c in range(count):
                draw.stamp()
                draw.fd(20)
            draw.right(90)

        # draw the obstacles
        draw.color("brown")
        draw.shapesize(stretch_len=0.5)
        for o in self.world.lstObstacles:
            draw.goto(self.base_x + (o.pos[0] * 20), self.base_y - (o.pos[1] * 20))
            draw.stamp()

    def update(self):
        # redraw the components that are likely to move around

        brain = self.world.tick() # evolve the state of the world

        # determine where to draw the player
        pBrain = self.world.player
        self.player.goto(self.base_x + (pBrain.pos[0] * 20), self.base_y - (pBrain.pos[1] * 20))
        if pBrain.choice == 0:
            self.player.seth(90)
        elif pBrain.choice == 1:
            self.player.seth(270)
        elif pBrain.choice == 2:
            self.player.seth(180)
        elif pBrain.choice == 3:
            self.player.seth(0)

        # determine where to draw the food and the predator
        self.food.goto(self.base_x + (self.world.food.pos[0] * 20), self.base_y - (self.world.food.pos[1] * 20))
        self.predator.goto(self.base_x + (self.world.predator.pos[0] * 20), self.base_y - (self.world.predator.pos[1] * 20))
        return brain


    def runSimulation(self, generationNum, agentNum):
        # visualize the simulation

        # if the visual components do not exist, create them
        if not self.worldExists:
            self.drawWorld()
            self.worldExists = True
        if self.pen is None:
            self.pen = turtle.Turtle()
            self.pen.penup()
            self.pen.speed(0)
            self.pen.goto((self.width / -2) + 10, (self.height / 2) - 10)
            self.pen.color("red")

        # write the current score of the current player
        self.pen.clear()
        self.pen.write(f"Gen: {generationNum}   Agent: {agentNum}")

        if self.food is None:
            self.food = turtle.Turtle()
            self.food.shape("circle")
            self.food.color("green")
            self.food.speed(0)
            self.food.penup()
            self.food.goto(self.base_x + (self.world.food.pos[0] * 20), self.base_y - (self.world.food.pos[1] * 20))

        if self.player is None:
            self.player = turtle.Turtle()
            self.player.shape("turtle")
            self.player.color("blue")
            self.player.speed(0)
            self.player.penup()
            self.player.goto(self.base_x + (self.world.player.pos[0] * 20), self.base_y - (self.world.player.pos[1] * 20))

        if self.predator is None:
            self.predator = turtle.Turtle()
            self.predator.shape("circle")
            self.predator.color("red")
            self.predator.speed(0)
            self.predator.penup()
            self.predator.goto(self.base_x + (self.world.predator.pos[0] * 20), self.base_y - (self.world.predator.pos[1] * 20))

        # begin the mainloop of the simulation
        brainData = self.update()
        while brainData is None:
            brainData = self.update()
            self.pen.clear()
            self.pen.write(f"Gen: {generationNum},    Agent: {agentNum}, score:{self.world.player.score}, {self.world.actions[self.world.player.choice]}, eats: {self.world.player.numEats}")
        return brainData
    
    def done(self):
        # close the instance of the screen and release all of the resources
        turtle.Screen().bye()
        self.worldExists = False
        self.pen = None
        self.food = None
        self.player = None
        self.predator = None
        try:
            self.screen = turtle.setup(self.width, self.height)
        except:
            pass
            # print("closed properly")



