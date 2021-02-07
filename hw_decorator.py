import random
from functools import wraps


# ЗАДАЧА-1
# Написать свой декоратор который будет проверять остаток от деления числа 100 на результат работы функции ниже.
# Если остаток от деления = 0, вывести сообщение "We are OK!», иначе «Bad news guys, we got {}» остаток от деления.
def division_by_one_hundred(func):
    """Decorator check the remainder of dividing 100 by the result of the function below """

    @wraps(func)
    def wrapper(*args, **kwargs):
        result_func = func(*args, **kwargs)
        if 100 % result_func == 0:
            print("We are OK!")
        else:
            print(f"Bad news guys, we got {100 % result_func}")
        return result_func

    return wrapper


@division_by_one_hundred
def random_choice_number():
    number = random.choice(range(0, 100))
    return number


# ЗАДАЧА-2
# Написать декоратор который будет выполнять предпроверку типа аргумента который передается в вашу функцию.
# Если это int, тогда выполнить функцию и вывести результат, если это str(),
# тогда зарейзить ошибку ValueError (raise ValueError(“string type is not supported”))
def check_given_data(func):
    """Decorator pre-checks the arguments passed to the function"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        given_data = [arg for arg in args if arg is not None] + \
                     [value for key, value in kwargs.items() if value is not None]
        if not given_data:
            raise ValueError("Current function hasn't any arguments or None")
        for data in given_data:
            if isinstance(data, str):
                raise ValueError("String type is not supported")
        return func(*args, **kwargs)

    return wrapper


@check_given_data
def divisible_by_given_divider(divider=2, start_sequences=0, finish_sequences=10):
    result_sequences = [char for char in range(start_sequences, finish_sequences) if char % divider == 0]
    return result_sequences


# ЗАДАЧА-3
# Написать декоратор который будет кешировать значения аргументов и результаты работы вашей функции и записывать
# его в переменную cache. Если аргумента нет в переменной cache и функция выполняется, вывести сообщение
# «Function executed with counter = {}, function result = {}» и количество раз сколько эта функция выполнялась.
# Если значение берется из переменной cache, вывести сообщение «Used cache with counter = {}» и
# количество раз обращений в cache.


def caching_functions_work(funk):
    """Decorator impemented process caching the results of executing the wrapped function"""

    @wraps(funk)
    def wrapper(*args, **kwargs):
        given_args = ''.join([str(arg) for arg in args if arg is not None])
        given_kwargs_step_1 = sorted([(key, value) for key, value in kwargs.items() if value is not None])
        given_kwargs_step_2 = ''.join([str(char) for unit in given_kwargs_step_1 for char in unit])
        given_data = given_args + given_kwargs_step_2
        if given_data in cache.keys():
            wrapper.counter_used_cache += 1
            print(f'Used cache with counter = {wrapper.counter_used_cache}')
            return cache[given_data]
        else:
            cache[given_data] = funk(*args, **kwargs)
            result = funk(*args, **kwargs)
            counter_funk_dict[funk] += 1
            print(f'Function executed with counter = {counter_funk_dict[funk]}, function result = {result}')
        print(cache)
        return funk(*args, **kwargs)

    counter_funk_dict = {}
    cache = {}
    counter_funk_dict[funk] = 0
    wrapper.counter_used_cache = 0
    return wrapper


@caching_functions_work
def fibonacci(n):
    if n in (1, 2):
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == '__main__':
    print('Task #1')
    result = random_choice_number()
    print(result)

    print('Task #2')
    result = divisible_by_given_divider(3, 10, 300)
    print(result)

    print('Task #3')
    result = fibonacci(40)
    print(result)
