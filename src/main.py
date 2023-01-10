from query import query_options
from colorama import init
import stories;
import storytime;

init(convert=True)

shouldPlayIntro = storytime.queryAndCheck("> Hello player, Would you like to view the intro?(Once it starts playing, it can not be skipped 🙃)\n>>  ", lambda s: s.lower().strip() in ['y', 'yes', 'ok', 'n', 'no', 'nope'], lambda s: f'<!> {s.strip()} is not a valid answer. Please answer with "yes" or "no".') in ['yes', 'y', 'ok']

if shouldPlayIntro:
    stories.introStory.startStory()

while True:
    """
    This is the main loop. It will run indefinitely.
    """

    query_options(True)