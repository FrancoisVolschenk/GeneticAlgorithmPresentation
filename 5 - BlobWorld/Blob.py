
class Blob:
    """This is the base class for the blob types which carries the common methods and properties"""
    def __init__(self, x = 0, y = 0, width = 10, height = 10, speed = 0.5, bearing = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = (255, 0, 0)
        self.speed = speed
        self.bearing = bearing
        self.energy = 100
        self.dead = False
        self.score = 0

    def decide_move(self, food_items):
        pass

    def crossover(self, other):
        pass

    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y