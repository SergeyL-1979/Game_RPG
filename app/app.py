from flask import Flask, render_template, redirect, request, url_for

from base import BaseUnit, Arena
from unit import PlayerUnit, EnemyUnit, UnitDied
from classes import unit_classes
from equipment import Weapon, Armor, Equipment


app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit,
}

arena = Arena()  # инициализируем класс арены


@app.route("/")
def menu_page():
    # рендерим главное меню (шаблон index.html)
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    # выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    # рендерим экран боя (шаблон fight.html)
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    # кнопка нанесения удара
    # обновляем экран боя (нанесение удара) (шаблон fight.html)
    # если игра идет - вызываем метод player.hit() экземпляра класса арены
    # если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
    # if arena.game_is_running:
    #     result = arena.player_hit()
    # else:
    #     result = arena.battle_result
    # return render_template('fight.html', heroes=heroes, result=result)
    # =====================================================================
    try:
        if arena.game_is_running:
            result = arena.player_hit()
        else:
            result = arena.battle_result
        # return render_template('fight.html', heroes=heroes, result=result)
    except UnitDied as e:
        error_unit = e.args[0]
        result = arena.battle_result
        return render_template('fight.html', heroes=heroes, result=result, error_unit=error_unit)
    return render_template('fight.html', heroes=heroes, result=result)



@app.route("/fight/use-skill")
def use_skill():
    # кнопка использования скилла
    # логика пркатикчески идентична предыдущему эндпоинту
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    # кнопка пропус хода
    # логика пркатикчески идентична предыдущему эндпоинту
    # однако вызываем здесь функцию следующий ход (arena.next_turn())
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    # кнопка завершить игру - переход в главное меню
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    # кнопка выбор героя. 2 метода GET и POST
    # на GET отрисовываем форму.
    # на POST отправляем форму и делаем редирект на эндпоинт choose enemy
    if request.method == 'GET':
        header = 'Выбор героя'
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes
        result = {'header': header,
                  "weapons": weapons,
                  "armors": armors,
                  "classes": classes}
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        heroes_name = request.form.get('name')
        heroes_weapon = request.form.get("weapon")
        heroes_armor = request.form.get("armor")
        unit_class = request.form.get("unit_class")

        player = PlayerUnit(name=heroes_name, unit_class=unit_classes.get(unit_class))
        player.equip_armor(Equipment().get_armor(heroes_armor))
        player.equip_weapon(Equipment().get_weapon(heroes_weapon))
        heroes['player'] = player
        return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    # кнопка выбор соперников. 2 метода GET и POST
    # также на GET отрисовываем форму.
    # а на POST отправляем форму и делаем редирект на начало битвы
    if request.method == 'GET':
        header = 'Выбор героя'
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes
        result = {'header': header,
                  "weapons": weapons,
                  "armors": armors,
                  "classes": classes}
        return render_template('hero_choosing.html', result=result)
    if request.method == 'POST':
        heroes_name = request.form.get('name')
        heroes_weapon = request.form.get("weapon")
        heroes_armor = request.form.get("armor")
        unit_class = request.form.get("unit_class")

        enemy = EnemyUnit(name=heroes_name, unit_class=unit_classes.get(unit_class))
        enemy.equip_armor(Equipment().get_armor(heroes_armor))
        enemy.equip_weapon(Equipment().get_weapon(heroes_weapon))
        heroes['enemy'] = enemy
        return redirect(url_for("start_fight"))


if __name__ == "__main__":
    app.run(debug=True, port=10000)
