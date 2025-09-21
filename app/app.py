# app/app.py
from __future__ import annotations
from flask import Flask, render_template, redirect, request, url_for

import random
from .base import Arena
from .unit import PlayerUnit, EnemyUnit, UnitDied
from .classes import unit_classes
from .equipment import Equipment

app = Flask(__name__)

heroes = {
    "player": None,
    "enemy": None,
}

arena = Arena()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/choose-hero/", methods=["GET", "POST"])
def choose_hero():
    scenario = request.args.get("scenario", "classic")
    eq = Equipment()
    result = {
        "header": "Выберите героя",
        "classes": list(unit_classes.keys()),
        "weapons": eq.get_weapons_names(),
        "armors": eq.get_armors_names(),
    }
    if request.method == "GET":
        return render_template("hero_choosing.html", result=result)

    name = request.form.get("name")
    weapon_name = request.form.get("weapon")
    armor_name = request.form.get("armor")
    unit_class_name = request.form.get("unit_class")

    # Игрок
    player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class_name))
    player.equip_weapon(eq.get_weapon(weapon_name))
    player.equip_armor(eq.get_armor(armor_name))
    heroes["player"] = player

    # Противник (рандомный класс и амуниция)
    enemy_class_name = random.choice(list(unit_classes.keys()))
    enemy_weapon = random.choice(eq.get_weapons_names())
    enemy_armor = random.choice(eq.get_armors_names())

    enemy = EnemyUnit(name="Противник", unit_class=unit_classes.get(enemy_class_name))
    enemy.equip_weapon(eq.get_weapon(enemy_weapon))
    enemy.equip_armor(eq.get_armor(enemy_armor))
    heroes["enemy"] = enemy

    return redirect(url_for("start_fight", scenario=scenario))


# вспомогательная функция для фиксации результата
def _ensure_battle_result():
    """Устанавливает результат боя и останавливает игру, если кто-то умер."""
    if not arena.game_is_running:
        return True
    if heroes["player"] and heroes["player"].hp <= 0 and heroes["enemy"] and heroes["enemy"].hp <= 0:
        arena.battle_result = "Ничья"
        arena.game_is_running = False
        return True
    if heroes["player"] and heroes["player"].hp <= 0:
        arena.battle_result = "Игрок проиграл"
        arena.game_is_running = False
        return True
    if heroes["enemy"] and heroes["enemy"].hp <= 0:
        arena.battle_result = "Игрок победил"
        arena.game_is_running = False
        return True
    return False

@app.route("/fight/")
def start_fight():
    scenario = request.args.get("scenario", "classic")
    arena.start_game(player=heroes["player"], enemy=heroes["enemy"], scenario=scenario)
    return render_template("fight.html", heroes=heroes, arena=arena)

@app.route("/fight/hit")
def hit():
    try:
        result = arena.player_hit()
    except UnitDied as e:
        result = str(e)
    if _ensure_battle_result():
        return redirect(url_for("fight_result"))
    return render_template("fight.html", heroes=heroes, arena=arena, result=result)

@app.route("/fight/use-skill")
def use_skill():
    try:
        result = arena.player_use_skill()
    except UnitDied as e:
        result = str(e)
    if _ensure_battle_result():
        return redirect(url_for("fight_result"))
    return render_template("fight.html", heroes=heroes, arena=arena, result=result)

@app.route("/fight/pass-turn")
def pass_turn():
    try:
        result = arena.next_turn()
    except UnitDied as e:
        result = str(e)
    if _ensure_battle_result():
        return redirect(url_for("fight_result"))
    return render_template("fight.html", heroes=heroes, arena=arena, result=result)

@app.route("/fight/end-fight")
def end_fight():
    arena.game_is_running = False
    arena.battle_result = arena.battle_result or "Бой завершён"
    return redirect(url_for("fight_result"))

# @app.route("/fight/result")
# def fight_result():
#     # на всякий случай выставим результат, если ещё пусто
#     _ensure_battle_result()
#     return render_template("result.html", heroes=heroes, arena=arena)
@app.route("/fight/result")
def fight_result():
    # если открыли страницу напрямую или после рестарта — отправим на главную
    if not heroes.get("player") or not heroes.get("enemy"):
        return redirect(url_for("index"))

    _ensure_battle_result()
    return render_template("result.html", heroes=heroes, arena=arena)
