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
    redundantWords: list[str] = ['towards', 'to', 'the', 'me', 'myself']; #LONGER WORDS SHOULD ALWAYS GO FIRST!

    def __init__(self):
        super().__init__("move", ["walk", "go"])

    def transformer(self, s: str):
        for word in self.redundantWords:
            s = s.replace(word, '')
        s = s.replace('  ', ' '); #replace double spaces that word removal might cause with single spaces.
        
        words = s.split(' ');

        index = 0;
        for word in words:
            
            if word == 'move' or word in self.aliases:
                break;
        
            index += 1;

        target = (' '.join(words[index + 1:len(words)])).strip();
        print(f"{target} is where they will move")

    def callback(self, direction: str):
        if direction in currentPlayer.currentNode and direction in builtNodes:
            currentPlayer.setNode(direction);
            return f"You walk to {direction}";
        else:
            return f"{direction} is not a valid location!"

commands = {
    "move": {
        "object": MoveCommand(),
    }
}