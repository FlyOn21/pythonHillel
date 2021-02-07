from functools import wraps
from datetime import datetime
import time
from sys import getsizeof
import json
from pprint import pprint


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
def my_lru_cache(max_size=4096):  # max cache size in bytes, default 4096 bytes
    def caching(funk):
        @wraps(funk)
        def wrapper(*args, **kwargs):
            # nonlocal cache
            result_func = funk(*args, **kwargs)
            input_args_kwargs = prepare_input_data(*args, **kwargs)
            cache = json_load()
            funk_key_str = f"{funk.__name__}"
            if funk_key_str in cache.keys():
                for unit in cache[funk_key_str]:
                    if input_args_kwargs in unit["input_args"]:
                        cache[f'cache_usage_{funk_key_str}'] += 1
                        unit["time"] = str(time.time())
                        json_dump(cache)
                        return unit["funk_do_values"]
            cache = clear_cache_on_overflow(cache, funk_key_str)
            pprint(cache)
            new_cache_unit = {"input_args": input_args_kwargs,
                              "funk_do_values": result_func,
                              "time": str(time.time())}
            if not funk_key_str in cache.keys():
                cache[f'cache_usage_{funk_key_str}'] = 0
                cache[funk_key_str] = []
                cache[f"usage_{funk.__name__}"] = 0
            cache[funk_key_str].append(new_cache_unit)
            cache[f"usage_{funk.__name__}"] += 1
            json_dump(cache)
            return result_func

        def cache_info():
            pass

        def json_dump(cache):
            with open('cache.json', 'w', encoding='UTF-8') as file:
                json.dump(cache, file, indent=2)

        def json_load():
            try:
                with open('cache.json', 'r', encoding='UTF-8') as file:
                    return json.load(file)
            except:
                cache = {}
                return cache

        def clear_cache_on_overflow(cache, funk_key_str, del_element=1):
            print(getsizeof(cache))
            if getsizeof(cache) <= max_size:
                return cache
            sorted_cache = sorted(cache[funk_key_str], key=lambda time: time['time'])
            print(sorted_cache)
            clear_sorted_cache = sorted_cache[:(len(sorted_cache) - del_element)]
            cache[funk] = clear_sorted_cache
            return cache

        def prepare_input_data(*args, **kwargs):
            input_args = ''.join([str(arg) for arg in args if arg is not None])
            input_kwargs_step_1 = sorted([(key, value) for key, value in kwargs.items() if value is not None])
            input_kwargs_step_2 = ''.join([str(char) for unit in input_kwargs_step_1 for char in unit])
            cache_key = input_args + input_kwargs_step_2
            return cache_key

        def cache_clear():
            pass

        # cache = json_load()
        # cache = {}
        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        # json_dump(cache)
        return wrapper

    return caching


#
#
# def decorator(my_func):
#     def wrapper():
#         my_func()
#
#     def cache_clear():
#         pass
#
#     wrapper.cache_clear = cache_clear
#     return wrapper
#
#
# @decorator
# def my_func():
#     pass
#
#
# my_func.cache_clear()

@my_lru_cache()
def fibonacci(n):
    if n in (1, 2):
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == "__main__":
    r = fibonacci(30)
    print(r)
