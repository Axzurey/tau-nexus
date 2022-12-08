from typing_extensions import TypedDict;
import time;
import re;

textView = tuple[str, float];


class storyLine():
    
    content: list[textView];

    @staticmethod
    def loadFromFile(filePath: str):
        content: list[textView] = [];
        with open(filePath, 'r') as f:

            i = 0;
            while True:
                i += 1;
                try:
                    line = f.readline();
                    if len(line) == 0 or line.isspace(): continue;

                    rex = re.compile(r"\[[+-]?\d+(?:\.\d+)?\]").search(line);

                    if not rex:
                        raise Exception(f"Error occured at line {i} of storybook {filePath}: Line numbering is malformed");

                    length = int(rex.group(0));
                    text = line[rex.start():];

                    content.append((text, length));

                except Exception as e:
                    raise Exception(f"Error occured at line {i} of storybook {filePath}: {str(e)}");
        f.close() #TODO
        return storyLine(content);


    def __init__(self, content: list[textView]) -> None:
        self.content = content;

    def startStory(self):
        for view in self.content:
            print(view[0]);
            time.sleep(view[1]);
