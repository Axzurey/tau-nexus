from __future__ import annotations
import random
from typing import TypedDict
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
    
    def __init__(self, name: str, params: NodeParams):
        """
        Node links aren't set in the constructor. Do not forget to set them explicitly via property annotation afterwards.
        """
        self.name = name
        self.connects = []
        self.params = params;

    def willEncounter(self) -> str | None:
        p = random.randrange(0, 100);
        if self.params["encounterChance"] > p: return; #they won't encounter anything!

        enemies = self.params['possibleEnemies'];


        c = random.random() * 100;
        cmt = 0;

        for enemy in enemies:
            cmt += enemies[enemy]
            if c < cmt:
                return enemy;

        raise Exception(f"[ILLEGAL STATE EXCEPTION] Sums of chances on node {self.name} do not sum up to 100%");

    def search(self):

        from playerNode import currentPlayer

        if self.areaSearches == self.params['maxSearches']: printinfo("You can not search this area any more!"); return;

        time.sleep(1);

        if self.searchedItems >= self.params["maxSearchedItems"]: printinfo("You can't find anything else, there is probably nothing left here"); return;
        
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

        currentPlayer.items.extend(out);

        printinfo("You rummage through the area and find " + ", ".join([f"""a{"n " if isSuffixedWithN(out[i].name) else " "}{out[i].name}" if i < len(out) - 1 else f"and a {out[i].name}""" for i in range(len(out))]));

        self.searchedItems += len(out);

builtNodes: dict[str, Node] = {}

builtNodes['origin'] = Node('Origin', {
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
    "encounterChance": 10,
})

builtNodes['house'] = Node('House', {
    "searchChances": {
        "elixir of life": 10,
        "elixir of brutality": 10,
        "basic sword": .2
    },
    "maxSearches": 3,
    "maxSearchedItems": 3,
    "possibleEnemies": {
        "small slime": 90,
        "big slime": 9.9,
        "very big slime": .1,
    },
    "encounterChance": 100
})


builtNodes['origin'].connects.append('house')
builtNodes['house'].connects.append('origin')