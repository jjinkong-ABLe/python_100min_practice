import math
import random


def circle_area(radius):
    return math.pi * radius ** 2


def pick_today_topic(topics):
    return random.choice(topics)


topics = ["variables", "strings", "lists", "loops", "functions"]

print("=== Built-in Modules ===")
print(f"Square root of 81: {math.sqrt(81)}")
print(f"Circle area: {circle_area(3):.2f}")
print(f"Today's topic: {pick_today_topic(topics)}")
