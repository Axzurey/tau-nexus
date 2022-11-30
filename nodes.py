from __future__ import annotations
from typing import Any
from statemachine import StateMachine, State

class Node(StateMachine, dict):
    connects: list[str] #str will be a name identifier for a node

    name: str

    locked: bool = False
    lockedReason: str = "This location is locked!"

    def __getattribute__(self, __name: str) -> Any:
        return super().__getattribute__(__name)
    
    def __init__(self, name: str):
        """
        Node links aren't set in the constructor. Do not forget to set them explicitly via property annotation afterwards.
        """
        self.name = name
        self.connects = []

builtNodes: dict[str, Node] = {}

builtNodes['origin'] = Node('origin')

builtNodes['house'] = Node('House')


builtNodes['origin'].connects.append('house')
builtNodes['house'].connects.append('origin')