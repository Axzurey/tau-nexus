from playerNode import currentPlayer
from commands import commands

def query_options():
    actions: list[str] = []
    walkableDirections: list[str] = []
    lockedDirections: dict[str, str] = {} #index is the cardinal direction, value is the reason it is locked

    for direction in ('north', 'south', 'east', 'west'):
        if hasattr(currentPlayer.currentNode, direction):
            print(direction)
            walkableDirections.append(direction) #for all the cardinal directions, if there is a node there, add it

    for item in currentPlayer.currentNode:
        print(item)

    if len(walkableDirections) >= 1:
        actions.append('move') #if they have somewhere to move to, let them know.

    outputMessage = """actions
------"""

    for action in actions:
        outputMessage += f"""
[{action}]{"(available directions): " + ", ".join(walkableDirections) if action == 'move' else ''}
"""
    if len(actions) == 0:
        print("You have no actions. This shouldn't happen, therefore the program will now exit")
        exit()

    query = input(outputMessage)