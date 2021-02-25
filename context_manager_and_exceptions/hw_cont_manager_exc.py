import os
import time
from contextlib import contextmanager, ContextDecorator
from itertools import permutations


# Задача-1
# Создать объект менеджера контекста который будет переходить в
# папку которую он принимает на вход. Так же ваш объект должен принимать
# исключение которое он будет подавлять Если флаг об исключении отсутствует, исключение должно быть поднято.


class MyContextManager():
    """Сlass implements the context manager structure for changing the current directory to the working directory"""

    def __init__(self, dirname, type_exception):
        self._work_dir_path = os.path.abspath(dirname)
        self._type_exception = type_exception
        self._current_dir_path = os.getcwd()

    def __enter__(self):
        if not os.path.isdir(self._work_dir_path):
            os.mkdir(self._work_dir_path)
        os.chdir(self._work_dir_path)
        print("Changed directory")

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self._current_dir_path)
        if exc_type is not None and issubclass(exc_type, self._type_exception):
            print("Directory not found")
            return True


# Задача -2
# Описать задачу выше но уже с использованием @contexmanager
@contextmanager
def my_context_manager(dirname, type_exception):
    """Function implements the context manager structure using a decorator contextmanager for changing
    the current directory to the working directory"""
    work_dir_path = os.path.abspath(dirname)
    current_dir_path = os.getcwd()
    if not os.path.isdir(work_dir_path):
        os.mkdir(work_dir_path)
    os.chdir(work_dir_path)
    print("Changed directory!!!")
    try:
        yield
    except type_exception:
        print("Directory not found")
    finally:
        os.chdir(current_dir_path)


# Задача -3
# Создать менеджер контекста который будет подсчитывать время выполнения вашей функции
class TimeExecutionFuncContextManager(ContextDecorator):
    """Class implements the structure of the context manager and also the ability to use it as a decorator
     for calculating the execution time of a function"""

    def __enter__(self):
        self._func_start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._execution_time = time.time() - self._func_start_time
        print("Function running time {:.4f}".format(self._execution_time))


@TimeExecutionFuncContextManager()
def all_permutations(sequence):
    result = [unit for unit in permutations(sequence)]
    return result


if __name__ == "__main__":
    print("Task #1")
    with MyContextManager("test_dir", FileNotFoundError):
        print(os.getcwd())
        os.rmdir(os.path.abspath("4.txt"))
    # print(os.getcwd())

    # print("Task #2")
    # with my_context_manager("test_dir", FileNotFoundError):
    #     print(os.getcwd())
    #     os.rmdir(os.path.abspath("test_dir_2"))
    # print(os.getcwd())
    #
    # print("Task #3")
    # permutations = all_permutations(range(10))
