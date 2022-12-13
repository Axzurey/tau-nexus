import os
from typing import Any, Literal
from item import ItemType, StatusItem, Item
from mathf import dictMergeInto, isInt, manySatisfy, mapToDict, parseNumberStr, printinfo, println, qInput, sequenceCount
from playerNode import currentPlayer
from nodes import builtNodes
from enemy import Enemy, enemies
import time
from colorama import Fore, Style
import random

Direction = Literal['north'] | Literal['south'] | Literal['east'] | Literal['west']

class Command():
    name: str
    aliases: list[str]

    def __init__(self, name: str, aliases: list[str]):
        self.name = name
        self.aliases = aliases

    def transformer(self, _s: str) -> bool:
        raise Exception("NOT IMPLEMENTED!")

    def callback(self):
        raise Exception("NOT IMPLEMENTED")

class MoveCommand(Command):
    """
    syntax: move to [location]
    paraphrasing is allowed, however only for specific words.
    """
    redundantWords: list[str] = ['towards', 'myself', 'node', 'back', 'to', 'the', 'me', 'my', 'an']; #LONGER WORDS SHOULD ALWAYS GO FIRST!

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
        
        return self.callback(target);

    def callback(self, direction: str):
        if direction in currentPlayer.currentNode.connects and direction in builtNodes:
            currentPlayer.setNode(direction);
            printinfo(f"You hastily walk to the {direction}");
            return "OK";
        elif direction in builtNodes:
            printinfo(f"You can not reach {direction} from here");
            return "BAD";
        else:
            printinfo(f"{direction} is not a valid location!");
            return "BAD";

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

        return node.search();

class BattleCommand(Command):
    def __init__(self):
        super().__init__("battle", ["attack", "fight"]);

    def transformer(self, enemyName: str):
        self.battleLoop(enemyName);

    def enemyAttack(self, enemy: Enemy):
        doesCrit = random.randrange(0, 100) < enemy.stats["critRate"]
        
        critDamageMul = enemy.stats["critMultiplier"];

        baseDamage = enemy.stats["attackRange"].calculateRandom();

        trueDamage = round(baseDamage * (critDamageMul if doesCrit else 1));

        currentPlayer.takeDamage(trueDamage);

        printinfo(f"The {enemy.name} attacks you for {trueDamage} damage");

        if currentPlayer.isDead():
            printinfo(f"GAME OVER: You died to a {enemy.name}");
            exit(); #the game ends. need I say more?
        else:
            printinfo(f"You now have {currentPlayer.stats['health']} health left");

    def battleLoop(self, enemyName: str):

        printinfo(f"You have now entered battle with {enemyName}")

        enemy = enemies[enemyName]['create']();

        turn = 0;

        time.sleep(1);

        while (True):
            turn += 1;

            time.sleep(.25);

            t = f"-----Turn {turn}-----";

            print(t + "-" * (os.get_terminal_size().columns - len(t)));

            res = self.battleRound(enemy);

            if res == "END":
                return;
            else:
                self.enemyAttack(enemy);

    
    def battleRound(self, enemy: Enemy):

        time.sleep(.5);
    
        q = qInput("""What would you like to do?
[attack the enemy]
[use an item]
[check your inventory]
[run away]
[inspect the enemy and yourself]""");

        def attack():
            doesCrit = random.randrange(0, 100) < currentPlayer.stats["critRate"]
            
            critDamageMul = currentPlayer.equippedWeapon.critMultiplier + currentPlayer.stats["critMultiplier"];

            baseDamage = currentPlayer.equippedWeapon.calculateDamage() + currentPlayer.stats['strength'];

            trueDamage = round(baseDamage * (critDamageMul if doesCrit else 1));

            enemy.takeDamage(trueDamage);

            printinfo(f"You attack the {enemy.name} for {trueDamage} damage!");

            time.sleep(.5);

            if enemy.isDead():
                printinfo(f"You killed the {enemy.name}, the battle is now over!");
                currentPlayer.currentNode.currentEnemy = None;
                return "END"
            else:
                printinfo(f"Your fairy informs you that the {enemy.name} now has {enemy.stats['health']} health");

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
                    else:
                        itemMatches.append(item); #type: ignore  OK, add it.
                else:
                    for subname in item.also:
                        s = subname;
                        for word in r:
                            s = s.replace(word, '');
                        s = s.replace(' ', '');

                        if s == target.replace(' ', ''):
                            if item.type != ItemType.STATUS:
                                printinfo("You can't use that item here because it isn't consumable!");
                                return self.battleRound(enemy);
                            else:
                                itemMatches.append(item); #type: ignore  OK, add it.

            if count > len(itemMatches):
                printinfo(f"You don't have that many {target}, you only have {len(itemMatches)}!");
                return self.battleRound(enemy);

            time.sleep(.25);

            for _ in range(count):
                p = itemMatches.pop();

                p.affect();

                currentPlayer.items.remove(p);

            printinfo(f"You use {count} {target}.");

            time.sleep(.25);

            return "PASS";

        def flee():
            printinfo("You promptly flee the scene to a random node");
            currentPlayer.setNode(random.choice(currentPlayer.currentNode.connects))
            time.sleep(.5)
            return "END";

        def inspect():
            time.sleep(.25)
            printinfo(f"Your fairy informs you that the {enemy.name} has {enemy.stats['health']} health.")
            time.sleep(.25)
            printinfo(f"Your fairy informs you that the you have {currentPlayer.stats['health']} health.")
            return "PASS";
        
        def printCHK():
            print(f"{Fore.MAGENTA}", end="");
            print(commands["inventory"]["object"].callback(True)); #type: ignore > It doesn't know.
            print(f"{Style.RESET_ALL}", end="");

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
                "callback": lambda: printCHK
            },
            "run": {
                "aliases": ["escape", "flee"],
                "callback": flee
            },
            "inspect": {
                "aliases": ['view'],
                "callback": inspect
            }
        }

        for substr in q.split(' '):
            for action in container:
                if substr.lower() == action or substr.lower() in container[action]['aliases']:
                    out = container[action]['callback']();
                    if out == "END":
                        return out;
                    elif out == "PASS":
                        return self.battleRound(enemy);
                    return;

        printinfo("That isn't a valid action. Try again.");

        return self.battleRound(enemy);

class InventoryCommand(Command):
    redundantWords: list[str] = [];

    def __init__(self):
        super().__init__("inventory", ["inv", "bag"]);

    def transformer(self, _s: str):
        res = self.callback();

        print(f"{Fore.MAGENTA}", end="");
        print(res); #type: ignore > It doesn't know.
        print(f"{Style.RESET_ALL}", end="");
        
        return "CTN"
        
    def callback(self, consumableOnly: bool = False):
        consumables = manySatisfy(currentPlayer.items, lambda item: item.type == ItemType.STATUS);
        weapons = manySatisfy(currentPlayer.items, lambda item: item.type == ItemType.WEAPON) if not consumableOnly else [];
        countedConsumables = sequenceCount([v.name for v in consumables]);
        countedWeapons = mapToDict([w.name for w in weapons], lambda _: 1); #doesn't need to stack so we'll just map em

        countedAll = dictMergeInto({}, [countedConsumables, countedWeapons]);

        z = [f"<#> {countedAll[k]}x {k}" for k in countedAll];

        s = "\n".join(z);

        return "<!> You have no items!" if len(countedAll) == 0 else s;

class EquipCommand(Command):

    redundantWords: list[str] = ['my', 'weapon', 'to', 'from', 'the', 'an'];

    def __init__(self):
        super().__init__("equip", ["switch"])

    def transformer(self, s: str):
        s = s.lower().strip();
        for word in self.redundantWords:
            s = s.replace(word, '')
        s = s.replace('  ', ' '); #replace double spaces that word removal might cause with single spaces.
        
        words = s.split(' ');

        index = 0;
        for word in words:
            
            if word == 'equip' or word in self.aliases:
                break;
        
            index += 1;

        target = (' '.join(words[index + 1:len(words)])).strip();

        if target == '':
            printinfo("You have not selected a valid item.");
            return "BAD";
        
        return self.callback(target);

    def callback(self, target: str):
        for item in currentPlayer.items:
            s = item.name;
            for word in self.redundantWords:
                s = s.replace(word, '');
            s = s.replace(' ', '');

            if s == target.replace(' ', ''):
                if item.type != ItemType.WEAPON:
                    printinfo("You can't use consumable items outside of battle");
                    return "BAD";
                else:
                    currentPlayer.items.append(currentPlayer.equippedWeapon); # Move their current weapon to their inventory
                    currentPlayer.equippedWeapon = item; #type: ignore > We know this must be a WeaponItem because of the above clause
                    currentPlayer.items.remove(item); # It should no longer be in their inventory
                    printinfo(f"Successfully equipped {target}");
                    return "CTN";
            else:
                for subname in item.also:
                    s = subname;
                    for word in self.redundantWords:
                        s = s.replace(word, '');
                    s = s.replace(' ', '');

                    if s == target.replace(' ', ''):
                        if item.type != ItemType.STATUS:
                            printinfo("You can't use consumable items outside of battle");
                            return "BAD"
                        else:
                            currentPlayer.items.append(currentPlayer.equippedWeapon); # Move their current weapon to their inventory
                            currentPlayer.equippedWeapon = item; #type: ignore > We know this must be a WeaponItem because of the above clause
                            currentPlayer.items.remove(item); # It should no longer be in their inventory
                            printinfo(f"Successfully equipped {target}");
                            return "CTN"

        printinfo(f"You don't have any {target}")
        return "BAD"

class StatusCommand(Command):
    def __init__(self):
        super().__init__("status", ["self"]);

    def transformer(self, _s):

        print(f"{Fore.MAGENTA}", end="");
        outS = '\n'.join([f'{i}: {currentPlayer.stats[i]}' for i in currentPlayer.stats]);
        print(f"{Style.RESET_ALL}", end="");

        printinfo(f"Your fairy calculates your status...");
        time.sleep(.25);
        print(outS);

class InspectCommand(Command):
    def __init__(self):
        super().__init__("inspect", []);

    def transformer(self, _s):

        outS = f"""<#> Name: {currentPlayer.equippedWeapon.name}
<#> Attack Damage (min, max): [{currentPlayer.equippedWeapon.damageRange.min}, {currentPlayer.equippedWeapon.damageRange.max}]
<#> Crit Multiplier: {currentPlayer.equippedWeapon.critMultiplier}""";

        printinfo(f"Your fairy appraises your weapon...");
        time.sleep(.25);
        print(f"{Fore.MAGENTA}", end="");
        print(outS);
        print(f"{Style.RESET_ALL}", end="");

class QuitCommand(Command):
    def __init__(self):
        super().__init__("quit", ["exit()"]);

    def transformer(self, _s: str):
        printinfo("The program will now exit. Bye");
        exit(0);

class HelpCommand(Command):
    redundantWords: list[str] = ["with", "my", "me", "the", "command", "to"];

    def __init__(self):
        super().__init__("help", ["assist"]);

    def transformer(self, s):
        s = s.lower().strip();
        for word in self.redundantWords:
            s = s.replace(word, '');
        s = s.replace('  ', ' '); #replace double spaces that word removal might cause with single spaces.
        
        words = s.split(' ');

        index = 0;
        for word in words:
            
            if word == 'help' or word in self.aliases:
                break;
        
            index += 1;

        target = (' '.join(words[index + 1:len(words)])).strip();

        targetCommand: str | None = None;
        
        for command in commands:
            cmd = commands[command]['object'];
            if command == target or target in cmd.aliases:
                targetCommand = command;
                break;

        if target != '' and not targetCommand:
            printinfo(f"Your fairy doesn't understand what {target} is.");
            return "BAD"
        elif targetCommand:
            printinfo(commandHelpCenter[targetCommand]);
        else:
            outS = '\n'.join([f"<#> {i}: {commandHelpCenter[i]}" for i in commandHelpCenter]);
            print(f"{Fore.MAGENTA}", end="");
            print(outS);
            print(f"{Style.RESET_ALL}", end="");


commandHelpCenter: dict[str, str] = {
    "move": """Allows you to move to an adjacent node.
Example usage: \"move to the forest\"""",
    "search": """Allows you to search your current node for items.
Example usage: \"search the area\"""",
    "battle": """When you encounter an enemy on a node, you can use this command to engage in battle.
Example usage: \"battle the enemy\"""",
    "inventory": """Allows you to view the items in your inventory.
Example usage: \"check my inventory\"""",
    "equip": """This command changes your equipped weapon.
Example usage: \"equip the sword of swords\"""",
    "status": """Displays your status.
Example usage: \"What's my status?\"""",
    "inspect": """Displays your weapon's stats
Example usage: \"inspect my weapon\"""",
    "help": """Brings up this message.
Example usage: \"help me\"""",
    "quit": """Exits the program.
Example usage: You don't need one(I hope)"""
}

commands: dict[str, dict[str, Command]] = {
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
    },
    "equip": {
        "object": EquipCommand(),
    },
    "status": {
        "object": StatusCommand(),
    },
    "inspect": {
        "object": InspectCommand(),
    },
    "help": {
        "object": HelpCommand(),
    },
    "quit": {
        "object": QuitCommand()
    }
}