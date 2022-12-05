import random;
from typing_extensions import Literal

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t;

def isInt(i: str):
    try:
        return int(i);
    except Exception:
        return False;

def parseNumberStr(n: str) -> tuple[Literal[True], int] | tuple[Literal[False], str]:
    """
    ex: parseNumberStr("twenty-five") -> 25
    ex: parseNumberStr("two-hundred-seventy-five") -> 275
    """

    ordinal0 = {
        "a": 1,
        "an": 1,
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
        "thirty": 30,
        "fourty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90,
    }

    ordinal1 = {
        "hundred": 100,
        "thousand": 1_000,
        "million": 1_000_000,
        "billion": 1_000_000_000,
        "trillion": 1_000_000_000_000
    }

    currentNumber = 0;

    s = n.split('-');
    
    m = 1;

    if s[0] in ordinal0 and len(s) > 1:
        m = int(s[0]);
    
    for i in range(len(s)):
        if m != 1 and i == 0: continue;

        if s[i] in ordinal0:
            currentNumber += ordinal0[s[i]] * m;
        elif s[i] in ordinal1:
            currentNumber += ordinal1[s[i]] * m;
        else:
            return (False, f"{s[i]} can not be interpreted as a number");

        if m != 1: m = 1;

    return (True, currentNumber);

class NumberRange():
    min: float;
    max: float;

    def __init__(self, min: float, max: float) -> None:
        self.min = min;
        self.max = max;

    def calculateRandom(self) -> float:
        return lerp(self.min, self.max, random.random()); #since random.randrange doesn't include endpoint. This is more complete i guess.