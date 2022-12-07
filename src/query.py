import os
from mathf import isSuffixedWithN, printinfo
from playerNode import currentPlayer
from commands import commands
import time

def query_options():
    actions: list[str] = ['search']

    if len(currentPlayer.currentNode.connects) >= 1:
        actions.append('move') #if they have somewhere to move to, let them know.

    qWillEncounter = currentPlayer.currentNode.willEncounter();

    print("-" * os.get_terminal_size().columns);

    if qWillEncounter:
        actions.append('battle');
    
    if len(actions) == 0:
        printinfo("You have no actions. This shouldn't happen, therefore the program will now exit")
        exit()

    if 'move' in actions:
        printinfo(f"Your fairy informs you of your surroundings: " + ", ".join([f"""{"an" if isSuffixedWithN(node) else "a"} {node}""" for node in currentPlayer.currentNode.connects]))
    if 'battle' in actions and qWillEncounter:
        printinfo(f"""You encounter a{"n " if isSuffixedWithN(qWillEncounter) else " "}{qWillEncounter}. What would you like to do?""")

    outputMessage = "\n".join([f"[{action}]" for action in actions]) + "\n>>  ";

    query = input(outputMessage);

    spl = query.split(' ');

    selectedCommand = 'NONE';

    i = -1;
    for word in spl:
        i += 1;
        for command in commands:
            if word == command or word in commands[command]['object'].aliases:
                selectedCommand = command;
                break;

    if selectedCommand == 'NONE':
        printinfo("It appears you have not selected a valid action. Please think it through and try again.");
        return query_options()
    elif selectedCommand == "battle":
        commands[selectedCommand]['object'].transformer(qWillEncounter);
    else:
        commands[selectedCommand]['object'].transformer(query);

    time.sleep(1.5); #give em some time before the next iteration
    