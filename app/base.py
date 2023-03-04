from unit import BaseUnit, UnitDied


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        # НАЧАЛО ИГРЫ -> None
        # присваиваем экземпляру класса аттрибуты "игрок" и "противник"
        # а также выставляем True для свойства "началась ли игра"
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        # ПРОВЕРКА ЗДОРОВЬЯ ИГРОКА И ВРАГА
        # проверка здоровья игрока и врага и возвращение результата строкой:
        # может быть три результата:
        # Игрок проиграл битву, Игрок выиграл битву, Ничья и сохраняем его в аттрибуте (self.battle_result)
        # если Здоровья игроков в порядке то ничего не происходит
        if self.player.hp > 0 and self.enemy.hp > 0:
            return None

        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = 'НИЧЬЯ'
        elif self.player.hp < 0:
            self.battle_result = f'{self.enemy.name} ПОБЕДИЛ!'
        else:
            self.battle_result = f'{self.player.name} ПОБЕДИЛ!'

    def _stamina_regeneration(self):
        # регенерация здоровья и регенерация выносливости(stamina_regeneration) для игрока и врага за ход
        # в этом методе к количеству выносливости(stamina) игрока и врага прибавляется константное значение.
        # главное чтобы оно не превысило максимальные значения (используйте if)
        units = (self.player, self.enemy)
        for unit in units:
            if unit.stamina + self.STAMINA_PER_ROUND > unit.unit_class.max_stamina:
                unit.stamina = unit.unit_class.max_stamina
            else:
                unit.stamina += self.STAMINA_PER_ROUND

    def next_turn(self):
        # СЛЕДУЮЩИЙ ХОД -> return result | return self.enemy.hit(self.player)
        # срабатывает когда игрок пропускает ход или когда игрок наносит удар.
        # создаем поле result и проверяем что вернется в результате функции self._check_players_hp
        # если result -> возвращаем его
        # если же результата пока нет и после завершения хода игра продолжается,
        # тогда запускаем процесс регенерации выносливости(stamina) и
        # здоровья для игроков (self._stamina_regeneration)
        # и вызываем функцию self.enemy.hit(self.player) - ответный удар врага
        result = self._check_players_hp()
        # self._check_players_hp()
        if result is not None:
            return result
        if self.game_is_running:
            self._stamina_regeneration()
            return self.enemy.hit(self.player)

    def _end_game(self):
        # КНОПКА ЗАВЕРШЕНИЕ ИГРЫ - > return result: str
        # очищаем синглтон - self._instances = {}
        # останавливаем игру (game_is_running)
        # возвращаем результат
        self._instances = {}
        self.game_is_running = False
        try:
            return self.battle_result
        except UnitDied as e:
            return f'{e.args[0]}'

    def player_hit(self):
        # КНОПКА УДАР ИГРОКА -> return result: str
        # получаем результат от функции self.player.hit
        # запускаем следующий ход
        # возвращаем результат удара строкой
        result = self.player.hit(self.enemy)
        turn_result = self.next_turn()
        return f'{result}<br>{turn_result}'

    def player_use_skill(self):
        # КНОПКА ИГРОК ИСПОЛЬЗУЕТ УМЕНИЕ
        # получаем результат от функции self.use_skill
        # включаем следующий ход
        # возвращаем результат удара строкой
        result = self.player.use_skill(self.enemy)
        turn_result = self.next_turn()
        return f'{result}<br>{turn_result}'
