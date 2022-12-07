from typing import Any, Literal
from item import ItemType, StatusItem, Item
from mathf import dictMergeInto, isInt, manyNotIn, manySatisfy, mapToDict, parseNumberStr, printinfo, println, sequenceCountByProperty
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

        print(words, target)
        
        res = self.callback(target);
        println(res);

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

        printinfo(f"You have now entered battle with {enemyName}")

        enemy = enemies[enemyName]['create']();

        turn = 0;

        time.sleep(1);

        while (True):
            turn += 1;

            printinfo(f"::Turn {turn}::");

            self.battleRound(enemy);
            time.sleep(.5);
    
    def battleRound(self, enemy: Enemy):
        q = input("""What would you like to do?
[attack the enemy]
[use an item]
[check your inventory]
[run away]
>>  """);

        def attack():
            doesCrit = currentPlayer.stats["critRate"] < random.randrange(0, 100)
            
            critDamageMul = currentPlayer.equippedWeapon.critMultiplier + currentPlayer.stats["critMultiplier"];

            baseDamage = currentPlayer.equippedWeapon.calculateDamage() + currentPlayer.stats['strength'];

            trueDamage = baseDamage * critDamageMul if doesCrit else 1;

            enemy.takeDamage(trueDamage);

            printinfo(f"You attack {enemy.name} for {trueDamage} damage!")

            time.sleep(1)

        def use():

            s = q; #copy it over, but don't mutate the original.

            r = ['the']

            s = s.lower().strip();
            for word in r:
                s = s.replace(word, '')
            s = s.replace('  ', ' '); #replace double spaces that word removal might cause with single spaces.
            
            words = s.split(' ');

            index = 0;

            count = 1;

            for word in words:
                
                if word == 'use':
                    break;
            
                index += 1;

            if index == len(words) - 1:
                printinfo("Unable to understand what you mean, please try again.");
                return self.battleRound(enemy);

            (pas, res) = parseNumberStr(words[index + 1]);

            if pas:
                count = int(res);
                words.pop(index + 1);
            elif isInt(words[index + 1]):
                count = isInt(words[index + 1]);
                words.pop(index + 1);

            target = (' '.join(words[index + 1:len(words)])).strip();

            itemMatches: list[StatusItem] = [];

            for item in currentPlayer.items:
                s = item.name;
                for word in r:
                    s = s.replace(word, '');
                s = s.replace(' ', '');

                if s == target.replace(' ', ''):
                    if item.type != ItemType.STATUS:
                        printinfo("You can't use that item here because it isn't consumable!");
                        return self.battleRound(enemy);

                    itemMatches.append(item); #type: ignore

                    return;

            if count > len(itemMatches):
                printinfo(f"You don't have that many {target}, you only have {len(itemMatches)}!");
                return self.battleRound(enemy);

            for _ in range(count):
                p = itemMatches.pop();

                currentPlayer.items.remove(p);

                #TODO

        container = {
            "attack": {
                "aliases": ['atk', 'fight'],
                "callback": attack
            },
            "use": {
                "aliases": [],
                "callback": use
            },
            "check": {
                "aliases": ["inventory", "inv"],
                "callback": lambda: print(commands["inventory"]["object"].callback())
            }
        }

        for substr in q.split(' '):
            for action in container:
                if substr.lower() == action or substr.lower() in container[action]['aliases']:
                    container[action]['callback']()
                    return;

        printinfo("That isn't a valid action. Try again.");

        return self.battleRound(enemy);

class InventoryCommand(Command):
    redundantWords: list[str] = [];

    def __init__(self):
        super().__init__("search", []);

    def transformer(self, _s: str):
        res = self.callback();
        println(res);
        
    def callback(self):
        consumables = manySatisfy(currentPlayer.items, lambda item: item.type == ItemType.STATUS);
        weapons = manySatisfy(currentPlayer.items, lambda item: item.type == ItemType.STATUS);
        countedConsumables = sequenceCountByProperty(consumables, "name");
        countedWeapons = mapToDict([w.name for w in weapons], lambda _: 1); #doesn't need to stack so we'll just map em

        countedAll = dictMergeInto({}, [countedConsumables, countedWeapons]);

        z = [f"<#> {countedAll[k]}x {k}" for k in countedAll];

        s = "\n".join(z);

        return "<!> You have no items!" if len(countedAll) == 0 else s;

commands = {
    "move": {
        "object": MoveCommand(),
    },
    "search": {
        "object": SearchCommand(),
    },
    "battle": {
        "object": BattleCommand(),
    },
    "inventory": {
        "object": InventoryCommand(),
    }
}