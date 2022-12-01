import random;

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t;

class NumberRange():
    min: float;
    max: float;

    def __init__(self, min: float, max: float) -> None:
        self.min = min;
        self.max = max;

    def calculateRandom(self) -> float:
        return lerp(self.min, self.max, random.random()); #since random.randrange doesn't include endpoint. This is more complete i guess.