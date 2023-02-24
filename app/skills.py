from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from unit import BaseUnit


class Skill(ABC):
    """
    Базовый класс умения
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self):
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough:
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    """
    Логика использования skill_effect -> return str
    В классе нам доступны экземпляры user и target - можно использовать любые их методы
    именно здесь происходит уменьшение stamina(выносливость) у игрока применяющего умение и
    уменьшение здоровья цели.
    Результат применения возвращаем строкой
    """
    name = 'Яростный удар'
    stamina = 6
    damage = 12

    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.target.get_damage(self.damage)
        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику."


class HardShot(Skill):
    """
    Логика использования skill_effect -> return str
    В классе нам доступны экземпляры user и target - можно использовать любые их методы
    именно здесь происходит уменьшение stamina(выносливость) у игрока применяющего умение и
    уменьшение здоровья цели.
    Результат применения возвращаем строкой
    """
    name = 'Жесткий выстрел'
    stamina = 5
    damage = 15

    def skill_effect(self) -> str:
        self.user.stamina -= self.stamina
        self.target.get_damage(self.damage)
        return f"{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику."