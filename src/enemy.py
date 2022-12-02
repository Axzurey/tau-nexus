from typing import TypedDict
import mathf;

class EnemyConstructor(TypedDict):
    health: float;
    maxHealth: float;
    attackRange: mathf.NumberRange;

class Enemy:

    stats: EnemyConstructor;
    
    def __init__(self, stats: EnemyConstructor):
        self.stats = stats;

    def takeDamage(self, dmg: float):
        self.stats['health'] -= dmg;

    def getAttack(self):
        return self.stats['attackRange'].calculateRandom();
    
    def isDead(self):
        return self.stats['health'] <= 0;

enemies = {
    "drunken man": {
        "create": lambda: Enemy({
            "health": 100,
            "maxHealth": 100,
            "attackRange": mathf.NumberRange(0, 5)
        })
    },
    "wolf": {
        "create": lambda: Enemy({
            "health": 50,
            "maxHealth": 50,
            "attackRange": mathf.NumberRange(5, 15)
        })
    },
    "small slime": {
        "create": lambda: Enemy({
            "health": 5,
            "maxHealth": 5,
            "attackRange": mathf.NumberRange(1, 2)
        })
    },
    "big slime": {
        "create": lambda: Enemy({
            "health": 70,
            "maxHealth": 70,
            "attackRange": mathf.NumberRange(15, 24)
        })
    },
    "very big slime": {
        "create": lambda: Enemy({
            "health": 120,
            "maxHealth": 120,
            "attackRange": mathf.NumberRange(25, 50)
        })
    }
}