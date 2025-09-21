# app/unit.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from .equipment import Weapon, Armor
from .classes import UnitClass

class UnitDied(Exception):
    pass

class BaseUnit(ABC):
    def __init__(self, name: str, unit_class: UnitClass):
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon: Optional[Weapon] = None
        self.armor: Optional[Armor] = None
        self._is_skill_used = False

    @property
    def health_points(self) -> float:
        return round(self.hp, 1)

    @property
    def stamina_points(self) -> float:
        return round(self.stamina, 1)

    @property
    def hp_display(self) -> float:
        # чтобы в шаблоне не показывать отрицательное
        return max(0.0, round(self.hp, 1))

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f"Игрок {self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"Игрок {self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: "BaseUnit") -> float:
        if self.weapon is None or target.armor is None:
            return 0.0
        if self.stamina < self.weapon.stamina_per_hit:
            return 0.0

        weapon_damage = self.weapon.damage * self.unit_class.attack

        armor_value = 0.0
        if target.stamina >= target.armor.stamina_per_turn:
            armor_value = target.armor.defence * target.unit_class.armor
            target.stamina -= target.armor.stamina_per_turn

        damage = max(0.0, round(weapon_damage - armor_value, 1))
        self.stamina -= self.weapon.stamina_per_hit
        return damage

    # def get_damage(self, damage: float) -> Optional[float]:
    #     if damage <= 0:
    #         return self.hp
    #     self.hp = round(self.hp - damage, 1)
    #     if self.hp <= 0:
    #         raise UnitDied(f"Трагически погиб в неравном бою {self.name}")
    #     return self.hp
    def get_damage(self, damage: float) -> Optional[float]:
        if damage <= 0:
            return self.hp
        self.hp = round(self.hp - damage, 1)
        if self.hp <= 0:
            self.hp = 0.0            # <<< не уходим в минус
            raise UnitDied(f"Трагически погиб в неравном бою {self.name}")
        return self.hp

    def use_skill(self, target: "BaseUnit") -> str:
        if self._is_skill_used:
            return "Навык уже использован."
        self._is_skill_used = True
        return self.unit_class.skill.use(self, target)

    @abstractmethod
    def hit(self, target: "BaseUnit") -> str:
        ...

class PlayerUnit(BaseUnit):
    def hit(self, target: "BaseUnit") -> str:
        if self.weapon is None or target.armor is None:
            return "Экипировка не выбрана."
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        damage = self._count_damage(target)
        if damage > 0:
            target.get_damage(damage)
            return f"{self.name}, используя {self.weapon.name}, пробивает {target.armor.name} соперника и наносит {damage} урона."
        return f"{self.name}, используя {self.weapon.name}, наносит удар, но {target.armor.name} соперника его останавливает."

class EnemyUnit(BaseUnit):
    def hit(self, target: "BaseUnit") -> str:
        if self.weapon is None or target.armor is None:
            return "Экипировка не выбрана."
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        damage = self._count_damage(target)
        if damage > 0:
            target.get_damage(damage)
            return f"{self.name}, используя {self.weapon.name}, пробивает {target.armor.name} и наносит {damage} урона."
        return f"{self.name}, используя {self.weapon.name}, наносит удар, но {target.armor.name} его останавливает."
