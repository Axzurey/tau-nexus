from typing import TypedDict
import mathf;

class EnemyConstructor(TypedDict):
    health: float;
    maxHealth: float;
    attackRange: mathf.NumberRange;
    critRate: float;
    critMultiplier: float;

class Enemy:

    name: str;

    stats: EnemyConstructor;
    
    def __init__(self, name: str, stats: EnemyConstructor):
        self.stats = stats;
        self.name = name;

    def takeDamage(self, dmg: float):
        self.stats['health'] -= dmg;

    def getAttack(self):
        return self.stats['attackRange'].calculateRandom();
    
    def isDead(self):
        return self.stats['health'] <= 0;

enemies = {
    "drunken man": {
        "create": lambda: Enemy("drunken man", {
            "health": 100,
            "maxHealth": 100,
            "attackRange": mathf.NumberRange(0, 5),
            "critRate": 10,
            "critMultiplier": 1.8,
        })
    },
    "wolf": {
        "create": lambda: Enemy("wolf", {
            "health": 50,
            "maxHealth": 50,
            "attackRange": mathf.NumberRange(5, 15),
            "critRate": 10,
            "critMultiplier": 1.25,
        })
    },
    "small slime": {
        "create": lambda: Enemy("small slime", {
            "health": 5,
            "maxHealth": 5,
            "attackRange": mathf.NumberRange(1, 2),
            "critRate": 1,
            "critMultiplier": 1.1,
        })
    },
    "big slime": {
        "create": lambda: Enemy("big slime", {
            "health": 70,
            "maxHealth": 70,
            "attackRange": mathf.NumberRange(15, 24),
            "critRate": 5,
            "critMultiplier": 1.2,
        })
    },
    "very big slime": {
        "create": lambda: Enemy("very big slime", {
            "health": 120,
            "maxHealth": 120,
            "attackRange": mathf.NumberRange(25, 50),
            "critRate": 12,
            "critMultiplier": 1.5,
        })
    }
}