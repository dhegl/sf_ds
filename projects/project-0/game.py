"""
  game.py

      Модуль реализации алгоритма поиска случайного числа
     на заданном диапазоне на основе игры "Угадай число".

     random_predict(verify)

        функция реализующая алгоритм "угадывания"

           verify - функция реализующая интерфейс "угадывания",
                    и подсчета количества попыток.

     score_game(random_predict)

         функция проверки, накопления и вывода статистики

             random_predict - функция реализующая алгоритм "угадывания"

         реализует так же внутреннюю функцию интерфейса "угадывания" (равно, больше, меньше)
         и подсчет количества попыток:

             verify_rnd_number(number)

                 number - "угадываемое" число

"""

import numpy as np

# по условию детерменированости != 0
RANDOM_SEED = 1
"""См. np.random.seed(). Zerro - seed setup off"""

#!!! Блок инициализации Г[П]СЧ перенесен из функции score_game()
if RANDOM_SEED:
    np.random.seed(RANDOM_SEED) # фиксируем сид для воспроизводимости

MAX_PASSES = 1000
"""Максимальное количество проходов проверки"""
MAX_RUNDOM_SIZE = 100
"""Максимальное загадываемое число"""
_DBG = 0
"""Вкл. отладочные принты"""

# для ограничения количества попыток
class GameOverError(OverflowError):
    pass

def score_game(random_predict) -> int:
    """
        За какое количество попыток в среднем из MAX_PASSES подходов угадывает наш алгоритм
    Args:
        random_predict (f: function([int])): функция угадывания
    Returns:
        int: среднее количество попыток
    """

    # список-ссылка на угадываемое число. (в замыкание)
    rnd_num_ref = [0]
    # счетчик попыток. (в замыкание)
    count_ref = [0]

    def verify_rnd_number(number:int=1) -> int:
        """
            Проверка числа на попадание
        Args:
            number (int, optional): Проверяемое число. Defaults to 1.

        Returns:
            int: 0 - если проверяемое число угадано
                 1 - если проверяемое число <меньше> загаданного
                -1 - если проверяемое число <больше> загаданного
        """
        nonlocal rnd_num_ref, count_ref

        if not type(number) is int:
            raise ValueError(f'value: [{number}] is not integer')
            #return None

        if count_ref[0] >= MAX_RUNDOM_SIZE:
            raise GameOverError('  Количество попыток "угадывания", увы, исчерпано :(')
        #TEST raise GameOverError('  Количество попыток "угадывания", увы, исчерпано :(')

        count_ref[0] += 1

        if rnd_num_ref[0] < number:
            return -1
        elif rnd_num_ref[0] > number:
            return 1
        else:
            return 0


    count_ls = [] # список для сохранения количества попыток

    if RANDOM_SEED:
        np.random.seed(RANDOM_SEED) # фиксируем сид для воспроизводимости

    random_array = np.random.randint(1, MAX_RUNDOM_SIZE + 1, size=(MAX_PASSES)) # загадали список чисел

    for number in random_array:
        #TODO: number -> rnd_num_ref[0] // Проверить
        rnd_num_ref[0] = number
        count_ref[0] = 0
        try:
        #
        # Запускаем наш "черный ящик" с функцией-ответчиком, фиксируем число "попыток"
        #
            random_predict(verify_rnd_number)
        #
        except Exception as e:
            print("\n\nОшибка выполнения \"random_predict()\" :")
            if isinstance(e, GameOverError):
                print(e)
                exit(1)
            else:
                #raise (e.with_traceback)
                raise e

        count_ls.append(count_ref[0])

    score = int(np.mean(count_ls))   # находим среднее количество попыток
    min_hits = min(count_ls)         # мин
    max_hits = max(count_ls)         # макс

    print(f'\nВаш алгоритм угадывает число в среднем за: {score} попыток. Мин: {min_hits} , Макс: {max_hits}\n')
    return score



def random_predict(verify:callable) -> int:
    """
        Рандомно угадываем число

    Args:
        verify : function(int)  функция проверяющая на попадание
            Принимает на вход угадывемое целое число.

            Дожна возвращать:
                0  - число угадано,
                1  - число больше предпологаемого,
                -1 - число меньше предпологаемого

    Returns:
        int: Число попыток
    """
    count = 0
    start_rnd_range = 1
    end_rnd_range = MAX_RUNDOM_SIZE

    # кол-во левых и правых "вилок"
    ch_rng_left  = 0
    ch_rng_right = 0

    while True:

        count += 1
        # случайное предполагаемое число
        predict_number = np.random.randint(start_rnd_range, end_rnd_range + 1)

        control = verify(predict_number)
        if control == 0:
            if _DBG:
                print(predict_number, ' - c:',count, ' <> ', ch_rng_left, ':', ch_rng_right)
            break
        elif control == 1:
            start_rnd_range = predict_number
            ch_rng_right += 1
        elif control == -1:
            end_rnd_range = predict_number
            ch_rng_left += 1
        else:
            raise ValueError("Control out of range. Mast be in [-1,0,1]")

    return count

# проверка random_predict(control_function)
if _DBG:
    _control_value = MAX_RUNDOM_SIZE // 2
    _control_verify = lambda x : 0 if x == _control_value else -1 if _control_value < x else 1
    print(f'Количество попыток: {random_predict(_control_verify)}')


if __name__ == "__main__":
    score_game(random_predict)
