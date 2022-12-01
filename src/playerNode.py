from __future__ import annotations
from typing import TypedDict
from nodes import Node, builtNodes
from item import Item

class PlayerStats(TypedDict):
    health: float;
    maxHealth: float;
    critRate: float;
    critMultiplier: float;

class PlayerNode():

    currentNode: Node;

    stats: PlayerStats;

    items: list[Item] = [];

    def __init__(self, startingNode: Node):
        self.currentNode = startingNode
        self.stats = {
            "health": 100,
            "maxHealth": 100,
            "critRate": 10,
            "critMultiplier": 1.5
        }

    def setNode(self, node: str):
        if node in builtNodes:
            self.currentNode = builtNodes[node]
        else:
            raise Exception(f"Node {node} does not exist!")

currentPlayer: PlayerNode = PlayerNode(builtNodes["origin"])