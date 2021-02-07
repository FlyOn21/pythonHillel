from functools import wraps
from datetime import datetime
import time


# LRU (least recently used) — это алгоритм, при котором вытесняются значения, которые дольше всего не запрашивались.
# Соответственно, необходимо хранить время последнего запроса к значению. И как только число закэшированных значений
# превосходит N необходимо вытеснить из кеша значение, которое дольше всего не запрашивалось.
#
#
# Задача - 1
# Создать декоратор lru_cache(подобный тому который реализован в Python).
#
# Задача-2
# Ваш lru_cache декоратор должен иметь служебный метод
# cache_info  - статистика использования вашего кеша(например: сколько раз вычислялась ваша функция,
# а сколько раз значение было взято из кеша, сколько места свободно в кеше)
#
# Задача-3
# Ваш lru_cache декоратор должен иметь служебный метод
# cache_clear - очищает кеш
#
# Пример обращения к служебному методу декоратора
def my_lru_cache(max_size=250):
    def caching(funk):
        @wraps(funk)
        def wrapper(*args, **kwargs):
            result_func = funk(*args, **kwargs)
            cache_key = prepare_input_data(*args, **kwargs)
            if funk in cache.keys():
                for unit in cache[funk]:
                    if cache_key in unit['key']:
                        unit['used'] += 1
                        unit['time'] = datetime.now()
                        return cache['value']

        def cache_info():
            pass

        def clear_cache_on_overflow():
            if len(cache) != max_size:
                return cache
            sorted_cache = sorted (cache,key=lambda time: time['time'])




        def prepare_input_data(*args, **kwargs):
            input_args = ''.join([str(arg) for arg in args if arg is not None])
            input_kwargs_step_1 = sorted([(key, value) for key, value in kwargs.items() if value is not None])
            input_kwargs_step_2 = ''.join([str(char) for unit in input_kwargs_step_1 for char in unit])
            cache_key = input_args + input_kwargs_step_2
            return cache_key

        def cache_clear():
            pass

        cache = {}
        free_cache_space = max_size - len(cache)
        dict_used_funk = {}
        # dict_funk_used_cache = {}
        dict_used_funk[funk] = 0
        # dict_funk_used_cache[funk] = 0
        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return wrapper

    return caching


def decorator(my_func):
    def wrapper():
        my_func()

    def cache_clear():
        pass

    wrapper.cache_clear = cache_clear
    return wrapper


@decorator
def my_func():
    pass


my_func.cache_clear()

if __name__ == "__main__":
    d = datetime.now()
    time.sleep(2)
    c = datetime.now()
    print(c - d)
