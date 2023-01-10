import random;
import time;
from collections.abc import Sequence, Callable
from typing_extensions import Literal;
from typing import TypeVar
from colorama import Fore, Style

T = TypeVar("T");
K = TypeVar("K");
V = TypeVar("V");

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t;

def isInt(i: str):
    try:
        return int(i);
    except Exception:
        return False;

def dictMergeInto(dict0: dict[K, T], dicts: list[dict[K, T]], overrideKeys: bool = False) -> dict[K, T]:
    """
    Joins keys from all dictionaries in dicts into dict0
    """
    for dict1 in dicts:
        for k in dict1:
            if k not in dict0 or overrideKeys:
                dict0[k] = dict1[k];

    return dict0;

def sequenceCount(seq: Sequence[K]) -> dict[K, int]:
    counter = {};

    for ind in seq:
        if ind in counter:
            counter[ind] += 1;
        else:
            counter[ind] = 1;

    return counter;

def mapToDict(seq: Sequence[T], fillValue: Callable[[T], V]) -> dict[T, V]:
    d = {};

    for item in seq:
        d[item] = fillValue(item);

    return d;

def manyNotIn(seq0: Sequence[T], seq1: Sequence[T]) -> list[T]:
    notIn = [];

    for s in seq0:
        if s not in seq1:
            notIn.append(s);

    return notIn;

def manySatisfy(seq: Sequence[T], check: Callable[[T], bool]) -> list[T]:
    satisfy = [];

    for s in seq:
        if check(s):
            satisfy.append(s);

    return satisfy;

def isSuffixedWithN(word: str) -> bool:
    """
    returns whether the given string should use "a" or "an"
    """
    return True if word[0] in ['a', 'e', 'i', 'o', 'u'] else False;

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


def flushInput():
    import msvcrt;
    while msvcrt.kbhit():
        msvcrt.getch();

def qInput(text: str, newline: bool = True):
    n = "\n";
    return input(f"""{text}{n if newline else ""}{Fore.CYAN}>>  {Style.RESET_ALL}""");

def println(s: int | float | str, timeLapse: float = 1):
    c = "> " + str(s);

    for char in c:
        print(char, flush=True, end="");
        time.sleep(timeLapse / len(c));
    print("");
    flushInput();

def printinfo(s: int | float | str, timeLapse: float = 1):
    c = "<!> " + str(s);

    print(f"{Fore.RED}", end="")

    for char in c:
        print(char, flush=True, end="");
        time.sleep(timeLapse / len(c));

    print(f"{Style.RESET_ALL}");

    flushInput();

def printStory(s: str | int | float, timeLapse: float = 1):
    c = str(s);

    print(f"{Fore.GREEN}", end="")

    for char in c:
        print(char, flush=True, end="");
        time.sleep(timeLapse / len(c));

    print(f"{Style.RESET_ALL}");