# app/base.py
from __future__ import annotations
from random import randint
from typing import Optional
from .unit import BaseUnit, UnitDied

class BaseSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1

    def __init__(self):
        self.player: Optional[BaseUnit] = None
        self.enemy: Optional[BaseUnit] = None
        self.game_is_running: bool = False
        self.battle_result: str = ""
        self.scenario: str = "classic"

    def start_game(self, player: BaseUnit, enemy: BaseUnit, scenario: str = "classic"):
        self.player, self.enemy = player, enemy
        self.game_is_running = True
        self.battle_result = ""
        self.scenario = scenario
        self.STAMINA_PER_ROUND = {"classic": 1, "fast": 3, "exhaustion": 0}.get(scenario, 1)

    def _stamina_regeneration(self):
        for unit in (self.player, self.enemy):
            if unit is None:
                continue
            gain = self.STAMINA_PER_ROUND * unit.unit_class.stamina
            unit.stamina = min(unit.unit_class.max_stamina, round(unit.stamina + gain, 1))

    def _check_players_hp(self) -> Optional[str]:
        if self.player is None or self.enemy is None:
            return None
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = "Ничья"
        elif self.player.hp <= 0:
            self.battle_result = "Игрок проиграл"
        elif self.enemy.hp <= 0:
            self.battle_result = "Игрок победил"
        else:
            return None
        return self._end_game()

    def _end_game(self) -> str:
        self.game_is_running = False
        return self.battle_result

    def next_turn(self) -> str:
        if not self.game_is_running:
            return self.battle_result

        result = self._check_players_hp()
        if result:
            return result

        self._stamina_regeneration()

        if self.player is None or self.enemy is None:
            return "Ошибка состояния боя."

        # 10% шанс умения у врага
        if (not self.enemy._is_skill_used) and randint(1, 10) == 1:
            enemy_action = self.enemy.use_skill(self.player)
        else:
            enemy_action = self.enemy.hit(self.player)

        end = self._check_players_hp()
        return enemy_action if not end else enemy_action + "<br>" + end

    def player_hit(self) -> str:
        if self.player is None or self.enemy is None:
            return "Ошибка состояния боя."
        result = self.player.hit(self.enemy)
        turn = self.next_turn()
        return result + "<br>" + turn

    def player_use_skill(self) -> str:
        if self.player is None or self.enemy is None:
            return "Ошибка состояния боя."
        result = self.player.use_skill(self.enemy)
        turn = self.next_turn()
        return result + "<br>" + turn
