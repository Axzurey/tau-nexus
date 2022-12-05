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

class Item:

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