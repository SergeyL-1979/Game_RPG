# app/skills.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .unit import BaseUnit

class Skill(ABC):
    user: "BaseUnit" = None
    target: "BaseUnit" = None
    name: str
    stamina: float
    damage: float

    def use(self, user: "BaseUnit", target: "BaseUnit") -> str:
        self.user, self.target = user, target
        if self.user.stamina < self.stamina:
            return f"{self.user.name} попытался использовать {self.name}, но у него не хватило выносливости."
        return self.skill_effect()

    @abstractmethod
    def skill_effect(self) -> str:
        ...

# БЫЛО
class FuryPunch(Skill):
    name = "Свирепый пинок"
    stamina = 6
    damage = 12
    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.target.get_damage(self.damage)
        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику."

class HardShot(Skill):
    name = "Мощный укол"
    stamina = 5
    damage = 15
    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.target.get_damage(self.damage)
        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику."

# ДОБАВЛЕНО
class CrushingBlow(Skill):
    name = "Сокрушительный удар"
    stamina = 8
    damage = 18
    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.target.get_damage(self.damage)
        return f"{self.user.name} обрушивает {self.name} и наносит {self.damage} урона!"

class FlurryStrikes(Skill):
    name = "Шквал ударов"
    stamina = 7
    damage = 14
    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.target.get_damage(self.damage)
        return f"{self.user.name} проводит {self.name}, суммарно нанося {self.damage} урона!"

class PreciseShot(Skill):
    name = "Точный выстрел"
    stamina = 5
    damage = 13
    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.target.get_damage(self.damage)
        return f"{self.user.name} делает {self.name} и наносит {self.damage} урона!"

class ArcaneBurst(Skill):
    name = "Чародейский взрыв"
    stamina = 8
    damage = 16
    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.target.get_damage(self.damage)
        return f"{self.user.name} высвобождает {self.name}, нанося {self.damage} урона!"
