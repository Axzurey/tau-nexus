from playerNode import currentPlayer
from commands import commands

def query_options():
    actions: list[str] = []
    lockedDirections: dict[str, str] = {} #index is the cardinal direction, value is the reason it is locked

    if len(currentPlayer.currentNode.connects) >= 1:
        actions.append('move') #if they have somewhere to move to, let them know.

    outputMessage = """actions
------"""

    for action in actions:
        outputMessage += f"""
[{action}]{"(available directions): " + ", ".join(currentPlayer.currentNode.connects) if action == 'move' else ''}
"""
    if len(actions) == 0:
        print("You have no actions. This shouldn't happen, therefore the program will now exit")
        exit()

    query = input(outputMessage)

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
        print("It appears you have not selected a valid action. Please think it through and try again.");
        return query_options()
    else:
        commands[selectedCommand]['object'].transformer(query);
    