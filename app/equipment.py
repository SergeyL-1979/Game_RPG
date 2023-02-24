from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: int  # выносливость за ход


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: int  # выносливость за удар

    @property
    def damage(self) -> float:
        return uniform(self.min_damage, self.max_damage)


@dataclass
class EquipmentData:
    #  содержит 2 списка - с оружием и с броней
    armors: List[Armor]
    weapons: List[Weapon]


class Equipment:
    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        # возвращает объект оружия по имени
        for weapon in self.get_weapons_names():
            if weapon.name == weapon_name:
            # if weapon_name == self.equipment['name']:
                return weapon
        raise NotImplementedError

    def get_armor(self, armor_name) -> Armor:
        # возвращает объект брони по имени
        for armor in self.get_armors_names():
            if armor.name == armor_name:
                return armor
        raise NotImplementedError

    def get_weapons_names(self) -> list:
        # возвращаем список с оружием
        return [item.name for item in self.equipment[0]]

    def get_armors_names(self) -> list:
        # возвращаем список с броней
        return [item.name for item in self.armor]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        # этот метод загружает json в переменную EquipmentData
        equipment_file = open("../data/equipment.json", encoding="utf-8")
        data = json.load(equipment_file)
        # print(data['weapons'][0]['name'])
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        # print(equipment_schema().dump(data)['weapons'])
        try:
            # return equipment_schema().dump(data)
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError


# d = Equipment()
# print(d.equipment['weapons'])
# print(d.equipment['armors'])
# print(d.equipment.weapons[0])
# print(d.equipment.armors[0])
