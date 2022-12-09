from typing import Callable;
import time;
import re;

textView = tuple[str, float];

def queryAndCheck(q: str, check: Callable[[str], bool], badInput: Callable[[str], str]) -> str:
    while True:
        i = input(q);
        if check(i):
            return i;
        else:
            print(badInput(i));

class storyLine():
    
    content: list[textView];

    @staticmethod
    def loadFromFile(filePath: str):
        content: list[textView] = [];
        with open(filePath, 'r', encoding="utf8") as f:

            i = 0;
            for line in f.readlines():
                i += 1;
                try:

                    if len(line) == 0 or line.isspace(): continue;

                    rex = re.compile(r"\[[+-]?\d+(?:\.\d+)?\]").search(line);

                    if not rex:
                        raise Exception(f"Error occured at line {i} of storybook {filePath}: Line numbering is malformed");

                    length = float(rex.group(0).replace('[', '').replace(']', ''));
                    text = f"> {line[rex.end():].strip()}"

                    content.append((text, length));

                except Exception as e:
                    raise Exception(f"Error occured at line {i} of storybook {filePath}: {str(e)}");

        f.close()
        return storyLine(content);


    def __init__(self, content: list[textView]) -> None:
        self.content = content;

    def startStory(self):
        for view in self.content:
            print(view[0]);
            time.sleep(view[1]);
