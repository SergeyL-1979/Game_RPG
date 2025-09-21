# app/equipment.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from random import uniform
import marshmallow_dataclass
import marshmallow
import json
import os

@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self) -> float:
        return round(uniform(self.min_damage, self.max_damage), 1)

@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float

@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]

equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)

class Equipment:
    def __init__(self, data_path: Optional[str] = None):
        self._data_path = data_path or os.path.join(
            os.path.dirname(__file__), "..", "data", "equipment.json"
        )
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Weapon:
        for w in self.equipment.weapons:
            if w.name == weapon_name:
                return w
        raise ValueError(f"Weapon '{weapon_name}' not found")

    def get_armor(self, armor_name: str) -> Armor:
        for a in self.equipment.armors:
            if a.name == armor_name:
                return a
        raise ValueError(f"Armor '{armor_name}' not found")

    def get_weapons_names(self) -> List[str]:
        return [w.name for w in self.equipment.weapons]

    def get_armors_names(self) -> List[str]:
        return [a.name for a in self.equipment.armors]

    def _get_equipment_data(self) -> EquipmentData:
        with open(self._data_path, encoding="utf-8") as f:
            data = json.load(f)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError as e:
            raise ValueError(f"Equipment JSON schema error: {e}")
