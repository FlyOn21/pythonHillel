import os
import time
from functools import wraps


# Задача-1
# У вас есть файл из нескольких строк. Нужно создать генератор который будет построчно выводить строки из вашего файла.
# При вызове итерировании по генератору необходимо проверять строки на уникальность.
# Если строка уникальна, тогда ее выводим на экран, если нет - скипаем


def unique_text_generator(data_file):
    """The generator produces one unique line from the file passed to
     it as input, if the line is repeated, then it is skipped"""
    list_line_file = []
    with open(os.path.abspath(data_file), "r", encoding="UTF8") as file:
        while True:
            one_line = file.readline()
            if not one_line:
                break
            if not one_line.strip() in list_line_file:
                list_line_file.append(one_line.strip())
                yield one_line


# Задача-2 (оригинальный вариант и его делать не обязательно):
# представим есть файл с логами, его нужно бессконечно контролировать
# на предмет возникнования заданных сигнатур.
#
# Необходимо реализовать пайплайн из корутин, который подключается к существующему файлу
# по принципу команды tail, переключается в самый конец файла и с этого момента начинает следить
# за его наполнением, и в случае возникнования запиcей, сигнатуры которых мы отслеживаем -
# печатать результат
#
# Архитектура пайплайна

#                    --------
#                   /- grep -\
# dispenser(file) <- - grep - -> pprint
#                   \- grep -/
#                    --------

# Структура пайплайна:
# ```
def coroutine(func):
    """Coroutine decorator"""
    @wraps(func)
    def wrapper(*args):
        result = func(*args)
        next(result)
        return result

    return wrapper


def follow(logfile, dispenser):
    """Main function that starts the pipeline for tracking the data of interest in the log file"""
    with open(logfile, "r", encoding="UTF8") as file:
        try:
            file.seek(0, 2)
            while True:
                line = file.readline()
                if not line:
                    time.sleep(1)
                    continue
                dispenser.send(line)
        except KeyboardInterrupt:
            print("Stop logfile tracking")


@coroutine
def dispenser(greps):
    """Tracked signature manager coroutine"""
    while True:
        current_line = yield
        for grep in greps:
            grep.send(current_line)


@coroutine
def grep(find_str, func_printer):
    """Coroutine for finding the required signature in the passed line"""
    while True:
        current_line = yield
        if find_str in current_line:
            func_printer.send(current_line)


@coroutine
def printer():
    """Coroutine for outputting the result to the screen
    if the required signature is found"""
    while True:
        current_line = yield
        print(current_line)


# ```
#
# Каждый grep следит за определенной сигнатурой
#
# Как это будет работать:
#
# ```
# f_open = open('log.txt')  # подключаемся к файлу
# follow(f_open,
#        # делегируем ивенты
#        dispenser([
#            grep('python', printer()),  # отслеживаем
#            grep('is', printer()),  # заданные
#            grep('great', printer()),  # сигнатуры
#        ])
#        )
# ```+-
# Как только в файл запишется что-то содержащее ('python', 'is', 'great') мы сможем это увидеть
#
# Итоговая реализация фактически будет асинхронным ивент хендлером, с отсутствием блокирующих операций.
#
# Если все плохо - план Б лекция Дэвида Бизли
# [warning] решение там тоже есть :)
# https://www.dabeaz.com/coroutines/Coroutines.pdf


# Задача-3 (упрощенный вариант делаете его если задача 2 показалась сложной)
# Вам нужно создать pipeline (конвеер, подобие pipeline в unix https://en.wikipedia.org/wiki/Pipeline_(Unix)).
#
# Схема пайплайна :
# source ---send()--->coroutine1------send()---->coroutine2----send()------>sink
#
# Все что вам нужно сделать это выводить сообщение о том что было получено на каждом шаге и обработку ошибки GeneratorExit.
#
# Например: Ваш source (это не корутина, не генератор и прочее, это просто функция ) в ней опеделите цикл из 10 элементов
# которые будут по цепочке отправлены в каждый из корутин и в каждом из корутив вызвано сообщение о полученном элементе.
# После вызова .close() вы должны в каждом из корутин вывести сообщение что работа завершена.

def source():
    counter = 0
    while counter <= 10:
        gen_first = coroutine_first()
        gen_first.send(counter)
        gen_first.close()
        counter += 1


@coroutine
def coroutine_first():
    try:
        while True:
            data = yield
            print(f"First coroutine received {data}")
            gen_seconds = coroutine_second()
            gen_seconds.send(data)
            gen_seconds.close()
    except GeneratorExit:
        print("First generator stop")


@coroutine
def coroutine_second():
    try:
        while True:
            data = yield
            print(f"Second coroutine received {data}")
            gen_sink = sink()
            gen_sink.send(data)
            gen_sink.close()
    except GeneratorExit:
        print("Second generator stop")


@coroutine
def sink():
    try:
        while True:
            data = yield
            print(f"Sink coroutine received {data}")
    except GeneratorExit:
        print("Sink generator stop")


if __name__ == "__main__":
    print("Task#1")
    gen = unique_text_generator("task#1.txt")
    for line in gen:
        print(line)

    print("Task#2")
    follow("logfile.txt", dispenser([
        grep('Python', printer()),
        grep('is', printer()),
        grep('great', printer()),
    ]))
    print("Task#3")
    source()
