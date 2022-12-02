from playerNode import currentPlayer
from commands import commands
import time

def query_options():
    actions: list[str] = ['search']

    if len(currentPlayer.currentNode.connects) >= 1:
        actions.append('move') #if they have somewhere to move to, let them know.

    outputMessage = """actions
------"""

    q = currentPlayer.currentNode.willEncounter();

    if q:
        actions.append('battle');

    for action in actions:
        outputMessage += f"""
[{action}]{"(available directions): " + ", ".join(currentPlayer.currentNode.connects) if action == 'move' else ''}
"""
    if len(actions) == 0:
        print("You have no actions. This shouldn't happen, therefore the program will now exit")
        exit()

    if 'battle' in actions:
        print(f"You encounter a(n) {q} What would you like to do?")

    query = input(outputMessage)

    spl = query.split(' ');

    selectedCommand = 'NONE';

    query = q if q else query;

    i = -1;
    for word in spl:
        i += 1;
        for command in commands:
            if word == command or word in commands[command]['object'].aliases:
                selectedCommand = command;
                break;

    if selectedCommand == 'NONE':
        print("It appears you have not selected a valid action. Please think it through and try again.");
        return query_options()
    else:
        commands[selectedCommand]['object'].transformer(query);

    time.sleep(1.5); #give em some time before the next iteration
    