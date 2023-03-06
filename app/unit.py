from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Equipment, Weapon, Armor
from classes import UnitClass, FuryPunch, HardShot
from skills import Skill
from random import randint
from typing import Optional


class UnitDied(Exception):
    pass


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health  # очки здоровья
        self.stamina = unit_class.max_stamina  # уровень выносливости
        self.weapon = None
        self.armor = None
        self._is_skill_used = False  # используется навык

    @property
    def health_points(self):
        # возвращаем аттрибут hp в красивом виде
        round(self.hp, 1)
        return f"Дорогой игрок {self.name} твой уровень здоровья ({self.hp})"

    @property
    def stamina_points(self):
        # возвращаем аттрибут hp в красивом виде
        round(self.stamina, 1)
        return f"Дорогой игрок {self.name} твоя выносливость ({self.stamina})"

    def equip_weapon(self, weapon: Weapon):
        # присваиваем нашему герою новое оружие
        self.weapon = weapon
        return f"Игрок {self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        # присваиваем нашему и одеваем новую броню
        self.armor = armor
        return f"Игрок {self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        # Эта функция должна содержать:
        #   логику расчета урона игрока
        #   логику расчета брони цели
        #   здесь же происходит уменьшение выносливости атакующего при ударе
        #   и уменьшение выносливости защищающегося при использовании брони
        #   если у защищающегося нехватает выносливости - его броня игнорируется
        #   после всех расчетов цель получает урон - target.get_damage(damage)
        #   и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде
        # =================================================================================
        # self.stamina -= self.weapon.stamina_per_hit
        # damage = self.weapon.damage * self.unit_class.attack
        #
        # if target.stamina >= target.armor.stamina_per_turn * target.unit_class.stamina:
        #     target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
        #     damage -= target.armor.defence * target.unit_class.armor
        #
        # damage = round(damage, 1)
        # target.get_damage(damage)
        # return damage
        # =================================================================================
        # Формула для расчета значения БРОНЯ_ЦЕЛИ
        weapon_damage = self.unit_class.attack * self.weapon.damage

        #   логику расчета брони цели
        # armor_goals = target.armor.defence * target.unit_class.stamina
        armor_goals = target.armor.defence * target.unit_class.armor
        self.stamina -= self.weapon.stamina_per_hit
        if target.stamina >= target.armor.stamina_per_turn * target.unit_class.stamina:
            weapon_damage -= target.armor.defence
            armor_goals -= target.armor.defence
            # self.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina

        target.get_damage(weapon_damage)
        return weapon_damage

    def get_damage(self, damage: int) -> Optional[float]:
        # получение урона целью присваиваем новое значение для аттрибута self.hp
        # self.hp -= damage  # - self.unit_class.stamina)
        if damage > 0:
            raise UnitDied(f'Трагически погиб в неравном бою {self.name}')
        return True
        # return self.hp
        # if damage > 0:
        #     self.hp -= damage

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        Этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        Метод использования умения.
        Если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку, которая характеризует выполнение умения

        Дам подсказку:
        У Skill есть метод _is_stamina_enough на проверку
        А также у BaseUnit есть параметр _is_skill_used
        """
        if self._is_skill_used:
            return '!!!!СУППЕР НАВЫК БЫЛ ИСПОЛЬЗОВАН!!!!'

        result = self.unit_class.skill.use(self, target)
        self._is_skill_used = True
        # return self.unit_class.skill.use(user=self, target=target)
        return result


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        Вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        # результат функции должен возвращать следующие строки:
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage <= self.stamina:
        # if damage > 0:
            return (
                f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
            )
        return (
            f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        )


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target)
        """
        if not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina and randint(0, 100) < 10:
            return self.use_skill(target)

        if self.stamina < self.weapon.stamina_per_hit:
            return f'{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости'

        # результат функции должен возвращать результат функции skill.use или же следующие строки:
        damage = self._count_damage(target)
        if damage <= self.stamina:
        # if damage > 0:
            return (
                f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
            )
        return (
            f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает.\n"
            # f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        )


# un = UnitClass(name='Player', max_health=100, max_stamina=20, attack=4, stamina=0.9, armor=2, skill=FuryPunch())
# un = UnitClass(name="Воин", max_health=100, max_stamina=20, attack=3, stamina=0.9, armor=2, skill=FuryPunch())
# player = PlayerUnit(name=un.name, unit_class=un)
#
# # un_en = UnitClass(name='Enemy', max_health=100, max_stamina=8, attack=7, stamina=0.9, armor=2, skill=HardShot())
# un_en = UnitClass(name="Вор", max_health=60,  max_stamina=15, attack=2, stamina=0.9, armor=0.7, skill=HardShot())
# enemy = EnemyUnit(name=un_en.name, unit_class=un_en)
# equipment = Equipment()
# player.equip_armor(armor=equipment.get_armor(equipment.get_armors_names()[1]))
# player.equip_weapon(weapon=equipment.get_weapon(equipment.get_weapons_names()[1]))
# enemy.equip_armor(armor=equipment.get_armor(equipment.get_armors_names()[1]))
# enemy.equip_weapon(weapon=equipment.get_weapon(equipment.get_weapons_names()[0]))
#
# try:
#     while all((player.health_points, enemy.health_points)):
#         print(enemy.hit(player))
#         print(player.hit(enemy))
# except UnitDied as e:
#     print(e.args[0])
#
#
# print('*' * 30)
# # print(player.health_points)
# # print(player.stamina_points)
# # print(enemy.health_points)
# # print(enemy.stamina_points)
# print(player.stamina, player.name, 'после удара')
# print(enemy.stamina, enemy.name, 'после удара')
# # print(player.get_damage(10))
# # print(player.get_damage(10))
# # print(player.get_damage(10))
# # print(player.get_damage(10))
#
# # print(enemy.use_skill(enemy))
# # print(enemy.hit(enemy))
# # un = UnitClass(name="Воин",
# #                max_health=100,
# #                max_stamina=20,
# #                attack=1,
# #                stamina=0.9,
# #                armor=2,
# #                skill=FuryPunch())
# #
# # un_en = UnitClass(name="Вор",
# #                   max_health=60,
# #                   max_stamina=15,
# #                   attack=2,
# #                   stamina=0.9,
# #                   armor=0.7,
# #                   skill=HardShot())
