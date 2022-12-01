from __future__ import annotations
import random
from typing import TypedDict
from item import Item, allItems

class NodeParams(TypedDict):
    
    searchChances: dict[str, float]; #chances are calculated individually
    maxSearches: int;

class Node(dict):
    connects: list[str]; #str will be a name identifier for a node

    name: str;

    locked: bool = False;
    lockedReason: str = "This location is locked!";

    areaSearches: int = 0;
    params: NodeParams;
    
    def __init__(self, name: str, params: NodeParams):
        """
        Node links aren't set in the constructor. Do not forget to set them explicitly via property annotation afterwards.
        """
        self.name = name
        self.connects = []
        self.params = params;

    def search(self):

        from playerNode import currentPlayer

        if self.areaSearches == self.params['maxSearches']: return "You can not search this area any more";
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

        print("You searched the area and found " + ", ".join([f"a {out[i].name}" if i < len(out) - 1 else f"and a {out[i].name}" for i in range(len(out))]));



builtNodes: dict[str, Node] = {}

builtNodes['origin'] = Node('origin', {
    "searchChances": {
        "health potion": 100,
        "mana potion": 100,
        "basic sword": 100
    },
    "maxSearches": 3,
})

builtNodes['house'] = Node('House', {
    "searchChances": {
        "health potion": 10,
        "mana potion": 10,
        "basic sword": .2
    },
    "maxSearches": 3,
})


builtNodes['origin'].connects.append('house')
builtNodes['house'].connects.append('origin')