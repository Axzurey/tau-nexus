from typing import Any, Literal
from playerNode import currentPlayer
from nodes import builtNodes

Direction = Literal['north'] | Literal['south'] | Literal['east'] | Literal['west']

class Command():
    name: str
    aliases: list[str]

    def __init__(self, name: str, aliases: list[str]):
        self.name = name
        self.aliases = aliases

    def transformer(self):
        raise Exception("NOT IMPLEMENTED!")

    def callback(self):
        raise Exception("NOT IMPLEMENTED")

class MoveCommand(Command):
    redundantWords: list[str] = ['to', 'direction']

    def __init__(self):
        super().__init__("move", ["walk"])

    def transformer(self, s: str):
        for word in self.redundantWords:
            s = s.replace(word, '')
        s = s.replace('  ', ' '); #replace double spaces that word removal might cause with single spaces.

    def callback(self, direction: str):
        if direction in currentPlayer.currentNode and currentPlayer.currentNode[direction]:
            targetNodeName = currentPlayer.currentNode['direction']
            if targetNodeName in builtNodes:
                currentPlayer.setNode(targetNodeName)
