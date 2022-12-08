class item(dict):
    def __init__(self, name: str) -> None:
        self.name = name;

class wepon(item):
    def __init__(self, name: str) -> None:
        super().__init__(name);

class cook(item):
    def __init__(self, name: str) -> None:
        super().__init__(name);

w, x, y, z = wepon('yes'), cook('hello'), item("bye"), wepon("no")

a: list[item] = [w, x, y, z]

print([v.name for v in a])

a.remove(x)

print([v.name for v in a])