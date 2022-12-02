from typing import Any, Literal
from playerNode import currentPlayer
from nodes import builtNodes
from enemy import Enemy, enemies
import time
import random

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
    """
    syntax: move to [location]
    paraphrasing is allowed, however only for specific words.
    """
    redundantWords: list[str] = ['towards', 'myself', 'node', 'back', 'to', 'the', 'me', 'my']; #LONGER WORDS SHOULD ALWAYS GO FIRST!

    def __init__(self):
        super().__init__("move", ["walk", "go"])

    def transformer(self, s: str):
        s = s.lower().strip();
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
        
        res = self.callback(target);
        print(res);

    def callback(self, direction: str):
        if direction in currentPlayer.currentNode.connects and direction in builtNodes:
            currentPlayer.setNode(direction);
            return f"You hastily walk to the {direction}";
        elif direction in builtNodes:
            return f"You can not reach {direction} from here";
        else:
            return f"{direction} is not a valid location!";

class SearchCommand(Command):
    """
    syntax: search
    no additional words are needed.
    """
    redundantWords: list[str] = [];

    def __init__(self):
        super().__init__("search", []);

    def transformer(self, _s: str):
        res = self.callback();
        
    def callback(self):
        node = currentPlayer.currentNode;

        node.search();

class BattleCommand(Command):
    def __init__(self):
        super().__init__("battle", ["attack", "fight"]);

    def transformer(self, enemyName: str):
        self.battleLoop(enemyName);

    def battleLoop(self, enemyName: str):

        print(f"You have now entered battle with {enemyName}")

        enemy = enemies[enemyName]['create']();

        turn = 0;

        time.sleep(1);

        while (True):
            turn += 1;

            print(f"::Turn {turn}::");

            self.battleRound(enemy);
            time.sleep(.5);
    
    def battleRound(self, enemy: Enemy):
        q = input("""What would you like to do?
[attack the enemy]
[use item]
[check bag]
[run away]
        """);

        def attack():
            doesCrit = currentPlayer.stats["critRate"] < random.randrange(0, 100)
            
            critDamageMul = currentPlayer.equippedWeapon.critMultiplier + currentPlayer.stats["critMultiplier"];

            baseDamage = currentPlayer.equippedWeapon.calculateDamage();

            trueDamage = baseDamage * critDamageMul if doesCrit else 1;

        container = {
            "attack": {
                "aliases": ['a', 'atk', 'fight'],
                "ignore": [],
                "callback": attack
            }
        }


commands = {
    "move": {
        "object": MoveCommand(),
    },
    "search": {
        "object": SearchCommand(),
    },
    "battle": {
        "object": SearchCommand()
    }
}