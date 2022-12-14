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

class Item():

    name: str;
    type: ItemType;
    also: list[str];

    def __init__(self, name: str, type: ItemType, also: list[str]):
        """
        the also argument, would be any aliases the item may have, including plural spellings.
        """
        self.name = name;
        self.type = type;
        self.also = also;

class WeaponItem(Item):

    damageRange: mathf.NumberRange;
    critMultiplier: float;
    
    def __init__(self, name: str, type: ItemType, also: list[str], params: WeaponItemConstructorParams):
        super().__init__(name, type, also);
        self.damageRange = mathf.NumberRange(params["damageMin"], params['damageMax']);
        self.critMultiplier = params['critMultiplier'];

    def calculateDamage(self):
        damage = self.damageRange.calculateRandom()

        return damage;

class StatusItem(Item):

    params: list[StatusFieldData]

    def __init__(self, name: str, type: ItemType, also: list[str], params: list[StatusFieldData]):
        super().__init__(name, type, also);

        self.params = params;

    def affect(self):

        from playerNode import currentPlayer;
        
        for data in self.params:

            currentPlayer.stats[data['stat']] *= data["increaseMul"]
            
            currentPlayer.stats[data['stat']] += data["increaseAdd"];
            


allItems = {
    "basic sword": {
        "type": "weapon",
        "create": lambda: WeaponItem("basic sword", ItemType.WEAPON, [], {
            "damageMin": 10,
            "damageMax": 15,
            "critMultiplier": 1.5,
        })
    },
    "sword of phantoms": {
        "type": "weapon",
        "create": lambda: WeaponItem("sword of phantoms", ItemType.WEAPON, ["sword of phantom"], {
            "damageMin": 25,
            "damageMax": 35,
            "critMultiplier": 1.55,
        })
    },
    "fish stick": {
        "type": "weapon",
        "create": lambda: WeaponItem("fish stick", ItemType.WEAPON, [], {
            "damageMin": 0.5,
            "damageMax": 1,
            "critMultiplier": 1,
        })
    },
    "basic axe": {
        "type": "weapon",
        "create": lambda: WeaponItem("basic axe", ItemType.WEAPON, [], {
            "damageMin": 20,
            "damageMax": 25,
            "critMultiplier": 1.75,
        })
    },
    "battle axe": {
        "type": "weapon",
        "create": lambda: WeaponItem("battle axe", ItemType.WEAPON, [], {
            "damageMin": 35,
            "damageMax": 40,
            "critMultiplier": 1.85,
        })
    },
    "sharp knife": {
        "type": "weapon",
        "create": lambda: WeaponItem("sharp knife", ItemType.WEAPON, [], {
            "damageMin": 17,
            "damageMax": 27,
            "critMultiplier": 1.55,
        })
    },
    "slightly sharper knife": {
        "type": "weapon",
        "create": lambda: WeaponItem("slightly sharper knife", ItemType.WEAPON, [], {
            "damageMin": 25,
            "damageMax": 35,
            "critMultiplier": 1.75,
        })
    },
    "absolute zero": {
        "type": "weapon",
        "create": lambda: WeaponItem("absolute zero", ItemType.WEAPON, [], {
            "damageMin": 0,
            "damageMax": 0,
            "critMultiplier": 0,
        })
    },
    "barett 50": {
        "type": "weapon",
        "create": lambda: WeaponItem("barett 50", ItemType.WEAPON, ["barett-50", "barett50"], {
            "damageMin": 40,
            "damageMax": 60,
            "critMultiplier": 3,
        })
    },
    "elixir of life": {
        "type": "status",
        "create": lambda: StatusItem("elixir of life", ItemType.STATUS, ['elixirs of life'], [
            {
                "increaseMul": 1,
                "increaseAdd": 25,
                "stat": "health"
            }
        ])
    },
    "elixir of brutality": {
        "type": "status",
        "create": lambda: StatusItem("elixir of brutality", ItemType.STATUS, ['elixirs of brutality'], [
            {
                "increaseMul": 1.1,
                "increaseAdd": 5,
                "stat": "strength"
            }
        ])
    },
    "elixir of intellect": {
        "type": "status",
        "create": lambda: StatusItem("elixir of intellect", ItemType.STATUS, ['elixirs of intellect'], [
            {
                "increaseMul": 1.25,
                "increaseAdd": .5,
                "stat": "critMultiplier"
            }
        ])
    },
    "finger of the fae": {
        "type": "status",
        "create": lambda: StatusItem("finger of the fae", ItemType.STATUS, ['fingers of the fae'], [
            {
                "increaseMul": 1.5,
                "increaseAdd": .8,
                "stat": "critMultiplier"
            }
        ])
    },
    "toe of the fae": {
        "type": "status",
        "create": lambda: StatusItem("toe of the fae", ItemType.STATUS, ['toes of the fae'], [
            {
                "increaseMul": 1.25,
                "increaseAdd": 30,
                "stat": "strength"
            }
        ])
    },
    "heart of the fae": {
        "type": "status",
        "create": lambda: StatusItem("heart of the fae", ItemType.STATUS, ['hearts of the fae'], [
            {
                "increaseMul": 2.5,
                "increaseAdd": 50,
                "stat": "health"
            }
        ])
    },
}