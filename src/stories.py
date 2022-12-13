import storytime;
import os;

introStory = storytime.storyLine.loadFromFile('src/storybook/backstory.txt')

pages: dict[str, storytime.storyLine] = {};

for dir in os.listdir('src/storybook/pages'):
    pages[dir.split('.')[0]] = storytime.storyLine.loadFromFile(f'src/storybook/pages/{dir}');