from typing import Any
from statemachine import StateMachine, State

class Node(StateMachine, dict):
    north: str | None
    east: str | None
    south: str | None
    west: str | None
    #the above are name identifiers for nodes. Optionally, they can be None

    name: str

    def __getattribute__(self, __name: str) -> Any:
        return super().__getattribute__(__name)
    
    def __init__(self, name: str):
        """
        Node links aren't set in the constructor. Do not forget to set them explicitly via property annotation afterwards.
        """
        self.name = name

builtNodes: dict[str, Node] = {}

builtNodes['origin'] = Node('origin')