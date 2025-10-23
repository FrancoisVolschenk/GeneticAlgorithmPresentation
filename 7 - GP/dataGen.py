import random
import math


def pythag_data():
    for i in range(10):
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        c = (a**2) + (b**2)
        print(f"{a},{b},{c}")


def sum():
    for i in range(10):
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        c = a + b
        print(f"{a},{b},{c}")


def dif():
    for i in range(10):
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        c = a - b
        print(f"{a},{b},{c}")


def eg():
    for i in range(10):
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        c = ((a - b) * (a + b)) + 5
        print(f"{a},{b},{c}")


def area_of_triangle_data():
    for i in range(10):
        width = random.randint(0, 100)
        perp_height = random.randint(0, 100)
        area = (0.5 * width) * perp_height
        print(f"{width},{perp_height},{area}")


def area_of_circle_data():
    for i in range(10):
        radius = random.randint(0, 100)
        junk = random.randint(0, 100)
        area = math.pi * (radius**2)
        print(f"{radius},{junk},{area}")


if __name__ == "__main__":
    selection = input(
        """
        (1): sum
        (2): Difference
        (3): Pythagorean theorem
        (4): Area of a triangle
        (5): Area of a circle
        (6): eg
        \n:"""
    )
    if selection == "1":
        sum()
    elif selection == "2":
        dif()
    elif selection == "3":
        pythag_data()
    elif selection == "4":
        area_of_triangle_data()
    elif selection == "5":
        area_of_circle_data()
    else:
        eg()
