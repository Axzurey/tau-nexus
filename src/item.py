from __future__ import annotations
import mathf;
from typing_extensions import TypedDict, NotRequired;
from enum import Enum

class WeaponItemConstructorParams(TypedDict):
    damageMin: float;
    damageMax: float;
    critMultiplier: float;

class StatusFieldData(TypedDict):
    increaseMul: float;
    increaseAdd: float;
    stat: str;

class ItemType(Enum):
    WEAPON = 1;
    STATUS = 2;

class Item(dict):

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)  # type: ignore

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)


    name: str;
    type: ItemType;

    def __init__(self, name: str, type: ItemType):
        self.name = name;
        self.type = type;

class WeaponItem(Item):

    damageRange: mathf.NumberRange;
    critMultiplier: float;
    
    def __init__(self, name: str, type: ItemType, params: WeaponItemConstructorParams):
        super().__init__(name, type);
        self.damageRange = mathf.NumberRange(params["damageMin"], params['damageMax']);
        self.critMultiplier = params['critMultiplier'];

    def calculateDamage(self):
        damage = self.damageRange.calculateRandom()

        return damage;

class StatusItem(Item):

    params: list[StatusFieldData]

    def __init__(self, name: str, type: ItemType, params: list[StatusFieldData]):
        super().__init__(name, type);

        self.params = params;

    def affect(self):

        from playerNode import currentPlayer;
        
        for data in self.params:

            currentPlayer.stats[data['stat']] *= data["increaseMul"]
            
            currentPlayer.stats[data['stat']] += data["increaseAdd"];
            


allItems = {
    "basic sword": {
        "type": "weapon",
        "create": lambda: WeaponItem("basic sword", ItemType.WEAPON, {
            "damageMin": 10,
            "damageMax": 15,
            "critMultiplier": 1.5,
        })
    },
    "elixir of life": {
        "type": "status",
        "create": lambda: StatusItem("elixir of life", ItemType.STATUS, [
            {
                "increaseMul": 1,
                "increaseAdd": 25,
                "stat": "health"
            }
        ])
    },
    "elixir of brutality": {
        "type": "status",
        "create": lambda: StatusItem("elixir of brutality", ItemType.STATUS, [
            {
                "increaseMul": 1.1,
                "increaseAdd": 5,
                "stat": "strength"
            }
        ])
    }
}