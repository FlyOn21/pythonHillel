import random
import time
from datetime import datetime
from functools import wraps


def time_do(funk):
    @wraps(funk)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = funk(*args, **kwargs)
        end_time = time.time()
        all_log = (f" Function name: {funk.__name__} ", f" Result: {result} ", f" Time do: {end_time - start_time} ")
        for unit in all_log:
            print(unit)
        with open('log.txt', 'a', encoding='UTF-8') as file:
            file.write((str(datetime.now()) + '|'))
            for log in all_log:
                file.write(log +"|")
            file.write("\n")
        return result

    return wrapper


@time_do
def random_choice_number():
    number = random.choice(range(0, 100))
    return number


if __name__ == '__main__':
    result = random_choice_number()
