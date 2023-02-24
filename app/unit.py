from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Equipment, Weapon, Armor
from classes import UnitClass, FuryPunch
from random import randint
from typing import Optional


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
        self._is_skill_used = False

    @property
    def health_points(self):
        # возвращаем аттрибут hp в красивом виде
        return f"Дорогой игрок {self.name} твой уровень здоровья ({self.hp})"

    @property
    def stamina_points(self):
        # возвращаем аттрибут hp в красивом виде
        return f"Дорогой игрок {self.name} твоя выносливость ({self.stamina})"

    def equip_weapon(self, weapon: Weapon):
        # присваиваем нашему герою новое оружие
        return f"Игрок {self.name} экипирован оружием {weapon.name}"

    def equip_armor(self, armor: Armor):
        # одеваем новую броню
        return f"Игрок {self.name} экипирован броней {armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        damage = 0
        #  TODO Эта функция должна содержать:
        #   логику расчета урона игрока
        #   логику расчета брони цели
        #   здесь же происходит уменьшение выносливости атакующего при ударе
        #   и уменьшение выносливости защищающегося при использовании брони
        #   если у защищающегося нехватает выносливости - его броня игнорируется
        #   после всех расчетов цель получает урон - target.get_damage(damage)
        #   и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде
        target.get_damage(damage)
        return damage

    def get_damage(self, damage: int) -> Optional[float]:
        # TODO получение урона целью присваиваем новое значение для аттрибута self.hp
        new_hp = self.stamina - damage
        return new_hp

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
        """
        return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        Вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        # результат функции должен возвращать следующие строки:
        if self._count_damage(target) >= self.stamina:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона." \
                   f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает." \
                   f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """
        # TODO результат функции должен возвращать результат функции skill.use или же следующие строки:
        return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона." \
               f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает." \
               f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

# d = UnitClass(name='Test', max_health=10, max_stamina=10, attack=4, stamina=10, armor=5, skill=FuryPunch())
# e = UnitClass(name='EEE', max_health=5, max_stamina=8, attack=7, stamina=8, armor=2, skill=FuryPunch())
# p = PlayerUnit(name='T', unit_class=d)
# ee = EnemyUnit(name='E', unit_class=d)
# print(p.hit(p))
