from dataclasses import dataclass
from skills import Skill, FuryPunch, HardShot


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass = UnitClass(
    name="Воин",
    max_health=100,
    max_stamina=20,
    attack=1,
    stamina=0.9,
    armor=2,
    skill=FuryPunch()
)  # Инициализируем экземпляр класса UnitClass и присваиваем ему необходимые значения аттрибутов

ThiefClass = UnitClass(
    name="Вор",
    max_health=60,
    max_stamina=15,
    attack=2,
    stamina=0.9,
    armor=0.7,
    skill=HardShot()
)  # действуем так же как и с воином

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}

u = unit_classes.get('Воин')
print(u.skill.name)
