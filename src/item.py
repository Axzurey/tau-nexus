from __future__ import annotations
import mathf;
from typing import TypedDict;

class WeaponItemConstructorParams(TypedDict):
    damageMin: float;
    damageMax: float;
    critMultiplier: float;

class StatusItemConstructorParams(TypedDict):
    maxHealthUp: float;
    critMultiplierUp: float;
    critChanceUp: float;
    healthUp: float;


class Item:

    name: str;

    def __init__(self, name: str):
        self.name = name;

class WeaponItem(Item):

    damageRange: mathf.NumberRange;
    critMultiplier: float;
    
    def __init__(self, name: str, params: WeaponItemConstructorParams):
        super().__init__(name);
        self.damageRange = mathf.NumberRange(params["damageMin"], params['damageMax']);
        self.critMultiplier = params['critMultiplier'];

    def calculateDamage(self, isCrit: float):
        damage = self.damageRange.calculateRandom() * self.critMultiplier if isCrit else 1;

        return damage;

class StatusItem(Item):

    def __init__(self, name: str):
        super().__init__(name)


allItems = {
    "basic sword": {
        "type": "weapon",
        "create": lambda: WeaponItem("basic sword", {
            "damageMin": 10,
            "damageMax": 15,
            "critMultiplier": 1.5,
        })
    },
    "health potion": {
        "type": "status",
        "create": lambda: StatusItem("health potion")
    },
    "mana potion": {
        "type": "status",
        "create": lambda: StatusItem("mana potion")
    }
}