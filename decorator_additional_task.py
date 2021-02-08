from functools import wraps
from datetime import datetime
import json
import os


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
def my_lru_cache(max_size=599):
    def caching(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            input_args_kwargs = prepare_input_data(*args, **kwargs)
            if func_key_str in cache:
                for unit in cache[func_key_str]:
                    if input_args_kwargs in unit["input_args"]:
                        cache[f'cache_usage_{func_key_str}'] += 1
                        unit["time"] = str(datetime.now())
                        json_dump(cache)
                        return unit["func_do_values"]
            result_func = func(*args, **kwargs)
            new_unit_in_cache = {"input_args": input_args_kwargs,
                                 "func_do_values": result_func,
                                 "time": str(datetime.now())}
            if not func_key_str in cache:
                cache[f"cache_usage_{func_key_str}"] = 0
                cache[f"usage_{func_key_str}"] = 0
                cache[func_key_str] = []
            cache[func_key_str].append(new_unit_in_cache)
            cache[f"usage_{func_key_str}"] += 1
            clear_cache_on_overflow(cache)
            json_dump(cache)
            return result_func

        def cache_info():
            try:
                free_cache_space = max_size - all_space_cache()
                calculated_func = cache[f"usage_{func_key_str }"]
                cache_usage = cache[f"cache_usage_{func_key_str }"]
                return (f"Function {func_key_str } is calculated {calculated_func}\nValue is taken from the"
                       f" cache {cache_usage}\nFree space in cache {free_cache_space}")
            except KeyError:
                return "Сache not found"

        def cache_clear():
            try:
                path = os.path.abspath(f'cache/cache_{func_key_str}.json')
                os.remove(path)
                print("Cache is cleared")
            except FileNotFoundError:
                print("Сache is already cleared")


        def json_dump(cache):
            try:
                with open(os.path.join(os.path.abspath(f'cache/cache_{func_key_str}.json')), 'w', encoding='UTF-8') as file:
                    json.dump(cache, file, indent=2)
            except FileNotFoundError:
                os.mkdir('cache')
                with open(os.path.join(os.path.abspath(f'cache/cache_{func_key_str}.json')), 'w', encoding='UTF-8') as file:
                    json.dump(cache, file, indent=2)

        def json_load():
            try:
                with open(f'cache/cache_{func_key_str}.json', 'r', encoding='UTF-8') as file:
                    return json.load(file)
            except FileNotFoundError:
                cache = {}
                return cache

        def all_space_cache():
            all_space = 0
            for key, value in cache.items():
                if isinstance(value, list):
                    all_space += len(value)
                all_space += 1
            return all_space

        def clear_cache_on_overflow(cache, del_element=1):
            all_space = all_space_cache()
            if all_space < max_size:
                return cache
            try:
                sorted_cache_values_func = sorted(cache[func_key_str], key=lambda time: time['time'],reverse=True)
                clear_sorted_cache = sorted_cache_values_func[:(len(sorted_cache_values_func) - del_element)]
                cache[func_key_str] = clear_sorted_cache
                json_dump(cache)
                return
            except KeyError:
                pass


        def prepare_input_data(*args, **kwargs):
            input_args = ''.join([str(arg) for arg in args if arg is not None])
            input_kwargs_step_1 = sorted([(key, value) for key, value in kwargs.items() if value is not None])
            input_kwargs_step_2 = ''.join([str(char) for unit in input_kwargs_step_1 for char in unit])
            cache_key = input_args + input_kwargs_step_2
            return cache_key

        func_key_str = f"{func.__name__}"
        cache = json_load()
        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return wrapper
    return caching

@my_lru_cache()
def fibonacci(n):
    if n in (1, 2):
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

@my_lru_cache()
def fibonacci_2(n):
    if n in (1, 2):
        return 1
    return fibonacci_2(n - 1) + fibonacci_2(n - 2)

@my_lru_cache()
def fibonacci_3(n):
    if n in (1, 2):
        return 1
    return fibonacci_3(n - 1) + fibonacci_3(n - 2)

if __name__ == "__main__":    
    func = fibonacci(400)
    print(func)
    
    metod_cache_info_1 = fibonacci.cache_info()
    print(metod_cache_info_1)

    
    func_2 = fibonacci_2(500)
    print(func_2)
    
    metod_cache_info_2 = fibonacci_2.cache_info()
    print(metod_cache_info_2)

    
    func_3 = fibonacci_3(600)
    print(func_3)
    
    metod_cache_info_3 = fibonacci_3.cache_info()
    print(metod_cache_info_3)

    metod_cache_clear_3 = fibonacci_3.cache_clear()
