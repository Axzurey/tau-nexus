from __future__ import annotations
import random
from typing import TypedDict
from enemy import Enemy
from item import Item, allItems
import time

from mathf import isSuffixedWithN, printinfo

class NodeParams(TypedDict):
    
    searchChances: dict[str, float]; #chances are calculated individually
    maxSearches: int;
    maxSearchedItems: int;
    possibleEnemies: dict[str, float] #chances of getting each enemy in the event of an encounter. values should add to 100
    encounterChance: float;

class Node():
    connects: list[str]; #str will be a name identifier for a node

    name: str;

    locked: bool = False;
    lockedReason: str = "This location is locked!";

    areaSearches: int = 0;
    searchedItems: int = 0;
    params: NodeParams;

    currentEnemy: str | None;

    onlyOneBattle: bool = False;

    visited: bool = False;

    firstTimeStoryId: str | None;
    
    def __init__(self, name: str, connects: list[str], params: NodeParams, firstTimeStoryId: str | None = None, onlyOneBattle: bool | None = None):
        """
        Node links aren't set in the constructor. Do not forget to set them explicitly via property annotation afterwards.
        """
        self.name = name
        self.connects = connects;
        self.params = params;
        self.currentEnemy = None;
        self.firstTimeStoryId = firstTimeStoryId;
        self.onlyOneBattle = onlyOneBattle or False;

    def willEncounter(self) -> str | None:

        if self.currentEnemy: return self.currentEnemy;

        p = random.randrange(0, 100);
        if p > self.params["encounterChance"]: return; #they won't encounter anything!

        enemies = self.params['possibleEnemies'];


        c = random.random() * 100;
        cmt = 0;

        for enemy in enemies:
            cmt += enemies[enemy]
            if c < cmt:
                self.currentEnemy = enemy;
                return enemy;

        raise Exception(f"[ILLEGAL STATE EXCEPTION] Sums of chances on node {self.name} do not sum up to 100%");

    def search(self):

        from playerNode import currentPlayer

        if self.areaSearches == self.params['maxSearches']: printinfo("You can not search this area any more!"); return "BAD";

        time.sleep(1);

        if self.searchedItems >= self.params["maxSearchedItems"]: printinfo("You can't find anything else, there is probably nothing left here"); return "BAD";
        
        self.areaSearches += 1;
        
        out: list[Item] = [];

        for itemName in self.params['searchChances'].keys():
            itemChance = self.params['searchChances'][itemName];
            
            pick = random.randrange(0, 100);
            if pick > itemChance:
                continue;
            
            if itemName not in allItems: raise Exception(f"Item {itemName} does not exist. This is a bug.");

            item = allItems[itemName]['create']();

            out.append(item);

        if len(out) == 0:
            printinfo("You search the area and find nothing");
        else:
            currentPlayer.items.extend(out);
            printinfo("You rummage through the area and find " + ", ".join([f"""a{"n " if isSuffixedWithN(out[i].name) else " "}{out[i].name}""" "" if i < len(out) - 1 else f"""and a{"n " if isSuffixedWithN(out[i].name) else " "}{out[i].name}""" for i in range(len(out))]));

        self.searchedItems += len(out);

builtNodes: dict[str, Node] = {}

builtNodes['grass patch'] = Node('grass patch', ["house"], {
    "searchChances": {
        "elixir of life": 100,
        "elixir of brutality": 100,
        "basic sword": 100
    },
    "maxSearches": 3,
    "maxSearchedItems": 3,
    "possibleEnemies": {
        "drunken man": 50,
        "wolf": 50
    },
    "encounterChance": 10
});

builtNodes['house'] = Node('house', ["grass patch", "city"], {
    "searchChances": {
        "elixir of life": 100,
        "elixir of brutality": 100,
        "battle axe": 30,
        "sharp knife": 30,
        "slightly sharper knife": 20
    },
    "maxSearches": 3,
    "maxSearchedItems": 3,
    "possibleEnemies": {
        "small slime": 50,
        "big slime": 49,
        "very big slime": 1,
    },
    "encounterChance": 100,
}, "bad_smell_house");

builtNodes['city'] = Node('city', ["house", "castle gates", "stable", "northern forest", "southern forest"], {
    "searchChances": {
        "elixir of life": 70,
        "elixir of brutality": 20,
        "battle axe": 30,
        "sharp knife": 30,
        "slightly sharper knife": 20
    },
    "maxSearches": 3,
    "maxSearchedItems": 3,
    "possibleEnemies": {
        "small slime": 50,
        "big slime": 49,
        "very big slime": 1,
    },
    "encounterChance": 100,
}, "city_ambient");

builtNodes['castle gates'] = Node('castle gates', ["city", "castle tower"], {
    "searchChances": {
        "elixir of life": 30,
        "elixir of brutality": 50,
        "battle axe": 20,
        "sharp knife": 50,
        "slightly sharper knife": 10
    },
    "maxSearches": 3,
    "maxSearchedItems": 3,
    "possibleEnemies": {
        "small slime": 50,
        "big slime": 49,
        "very big slime": 1,
    },
    "encounterChance": 100,
}, "castle_gates");

builtNodes['castle tower'] = Node('castle tower', ["castle gates"], {
    "searchChances": {
        "elixir of intellect": 30,
        "absolute zero": 100,
        "barret 50": 1,
    },
    "maxSearches": 3,
    "maxSearchedItems": 3,
    "possibleEnemies": {
        "big bad wizard": 100
    },
    "encounterChance": 100,
}, "castle_tower", True);

builtNodes['stable'] = Node('stable', ["city"], {
    "searchChances": {
        "sword of phantoms": 40,
        "fish stick": 90,
        "sharp knife": 30,
    },
    "maxSearches": 3,
    "maxSearchedItems": 3,
    "possibleEnemies": {
        "small slime": 50,
        "big slime": 49,
        "very big slime": 1,
    },
    "encounterChance": 100,
}, "very_bad_stable");

builtNodes['southern forest'] = Node('southern forest', ["city"], {
    "searchChances": {
        "elixir of life": 100,
        "elixir of brutality": 15,
        "battle axe": 20,
        "sharp knife": 60,
        "slightly sharper knife": 21
    },
    "maxSearches": 3,
    "maxSearchedItems": 3,
    "possibleEnemies": {
        "slightly angry nymph": 40,
        "very angry nymph": 40,
        "nymph bearing murderous intent": 20,
    },
    "encounterChance": 50,
}, "beautiful_forest");

builtNodes['northern forest'] = Node('northern forest', ["city"], {
    "searchChances": {
        "finger of the fae": 10,
        "toe of the fae": 10,
        "heart of the fae": 10,
    },
    "maxSearches": 3,
    "maxSearchedItems": 3,
    "possibleEnemies": {
        "dark elf": 49,
        "elf": 50,
        "elf that aims to become the next demon king": 1
    },
    "encounterChance": 50,
}, "dangerous_forest");