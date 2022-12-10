import os
from mathf import isSuffixedWithN, printinfo
from playerNode import currentPlayer
from commands import commands
import time

def query_options(firstPass: bool = False):
    actions: list[str] = ['search', 'inventory', 'equip', 'status']

    if len(currentPlayer.currentNode.connects) >= 1:
        actions.append('move') #if they have somewhere to move to, let them know.

    qWillEncounter = currentPlayer.currentNode.willEncounter();

    print("-" * os.get_terminal_size().columns);

    if qWillEncounter:
        actions.append('battle');
    
    if len(actions) == 0:
        printinfo("You have no actions. This shouldn't happen, therefore the program will now exit")
        exit()

    if 'move' in actions and firstPass:
        printinfo(f"Your fairy informs you of your surroundings: " + ", ".join([f"""{"an" if isSuffixedWithN(node) else "a"} {node}""" for node in currentPlayer.currentNode.connects]))
    if 'battle' in actions and qWillEncounter and firstPass:
        printinfo(f"""You encounter a{"n " if isSuffixedWithN(qWillEncounter) else " "}{qWillEncounter}.""")

    #outputMessage = "\n".join([f"[{action}]" for action in actions]) + "\n>>  ";

    outputMessage = "What would you like to do?(input help for more information)\n>>  " if firstPass else ">>  ";

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
        if selectedCommand: break;

    if selectedCommand == 'NONE':
        printinfo("It appears you have not selected a valid action. Please think it through and try again.");
        return query_options()
    elif selectedCommand == "battle":
        if qWillEncounter:
            commands[selectedCommand]['object'].transformer(qWillEncounter);
        else:
            printinfo("There's nothing there! are you trying to fight your demons?");
    else:
        o = commands[selectedCommand]['object'].transformer(query);
        if o == "BAD":
            return query_options()

    time.sleep(1.5); #give em some time before the next iteration
    