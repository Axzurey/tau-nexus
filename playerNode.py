from statemachine import StateMachine, State

from nodes import Node, builtNodes

class PlayerNode(StateMachine):

    currentNode: Node

    def __init__(self, startingNode: Node):
        self.currentNode = startingNode

    def setNode(self, node: str):
        if node in builtNodes:
            self.currentNode = builtNodes[node]
        else:
            raise Exception(f"Node {node} does not exist!")

currentPlayer: PlayerNode = PlayerNode(builtNodes["origin"])