from query import query_options
import storytime;

storytime.storyLine.loadFromFile('src/storybook/backstory.txt').startStory()

while True:
    """
    This is the main loop. It will run indefinitely.
    """

    query_options()