import random


class Food:
    """This is the food that will be scattered around the world for the blobs to eat"""
    def __init__(self, world_width = 0, world_height = 0, radius = 5):
        self.world_width = world_width
        self.world_height = world_height
        self.x = random.randint(0, world_width)
        self.y = random.randint(0, world_height)
        self.colour = (255, 0, 0)
        self.radius = radius

    def eat(self):
        """When eaten, respawn somewhere else"""
        self.x = random.randint(0, self.world_width)
        self.y = random.randint(0, self.world_height)