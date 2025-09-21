# app/classes.py
from __future__ import annotations
from dataclasses import dataclass
from .skills import Skill, FuryPunch, HardShot, CrushingBlow, FlurryStrikes, PreciseShot, ArcaneBurst

@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float        # множитель урона (оружие * attack)
    stamina: float       # множитель восстановления за ход (арена.STAMINA_PER_ROUND * stamina)
    armor: float         # множитель брони (defence * armor)
    skill: Skill

# БАЗОВЫЕ
WarriorClass = UnitClass(
    name="Воин",
    max_health=100,
    max_stamina=20,
    attack=1.0,
    stamina=0.9,
    armor=2.0,
    skill=FuryPunch()
)

ThiefClass = UnitClass(
    name="Вор",
    max_health=60,
    max_stamina=15,
    attack=2.0,
    stamina=0.9,
    armor=0.7,
    skill=HardShot()
)

# НОВЫЕ
PaladinClass = UnitClass(
    name="Паладин",
    max_health=120,
    max_stamina=18,
    attack=1.2,
    stamina=0.8,
    armor=2.5,
    skill=CrushingBlow()
)

RangerClass = UnitClass(
    name="Следопыт",
    max_health=80,
    max_stamina=18,
    attack=1.6,
    stamina=1.0,
    armor=1.2,
    skill=PreciseShot()
)

BerserkerClass = UnitClass(
    name="Берсерк",
    max_health=90,
    max_stamina=22,
    attack=2.2,
    stamina=0.7,
    armor=0.8,
    skill=FlurryStrikes()
)

MageClass = UnitClass(
    name="Маг",
    max_health=70,
    max_stamina=24,
    attack=2.0,
    stamina=1.1,
    armor=0.5,
    skill=ArcaneBurst()
)

unit_classes = {
    WarriorClass.name: WarriorClass,
    ThiefClass.name: ThiefClass,
    PaladinClass.name: PaladinClass,
    RangerClass.name: RangerClass,
    BerserkerClass.name: BerserkerClass,
    MageClass.name: MageClass
}
