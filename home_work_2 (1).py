import random
from collections import Counter
from functools import reduce
import pprint


# 1) Сгенерировать dict() из списка ключей ниже по формуле (key : key* key).keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# ожидаемый результат: {1: 1, 2: 4, 3: 9 …}


def dict_generations(keys=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
    """Функция генерирует словарь по заданому шаблону (key : key* key)"""
    new_dict = {key: key * key for key in keys}
    return new_dict


# 2) Сгенерировать массив(list()). Из диапазона чисел от 0 до 100 записать в результирующий массив только четные числа.
def list_generations():
    """Функция генерирует список в диапозоне от 0 до 100 содержащий четные числа"""
    new_list = [x for x in range(0, 100) if x % 2 == 0]
    return new_list


# 3)Заменить в произвольной строке согласные буквы на гласные.

def change_consonants_to_vowels(change_string='The same concept exists for classes, but is less commonly used there.'):
    """Функция заменяет согласные буквы в строке на гласные"""
    vowels = ('a', 'e', 'i', 'o', 'u', 'y')
    change_string_lower = change_string.lower()
    list_character = []
    for character in change_string_lower:
        if character == ' ':
            list_character.append(character)
        elif character in vowels:
            list_character.append(character)
        elif character not in vowels:
            character = random.choice(vowels)
            list_character.append(character)
    result_string = ''.join(list_character)
    return result_string


# 4)Дан массив чисел.[10, 11, 2, 3, 5, 8, 23, 11, 2, 5, 76, 43, 2, 32, 76, 3, 10, 0, 1]
# array = [10, 11, 2, 3, 5, 8, 23, 11, 2, 5, 76, 43, 2, 32, 76, 3, 10, 0, 1]


# 4.1) убрать из него повторяющиеся элементы
def remove_duplicate_units(array=[10, 11, 2, 3, 5, 8, 23, 11, 2, 5, 76, 43, 2, 32, 76, 3, 10, 0, 1]):
    """Функция удаляет дубликаты в массиве значений"""
    result = [unit for unit in set(array)]
    return result


# 4.2) вывести 3 наибольших числа из исходного массива
def three_max_unit(array=[10, 11, 2, 3, 5, 8, 23, 11, 2, 5, 76, 43, 2, 32, 76, 3, 10, 0, 1]):
    """Функция возвращает 3 наибольших значения из массива"""
    # prepared_array = remove_duplicate_units(array)
    step = 0
    result_unit_value = []
    while step < 3:
        max_value = max(array)
        result_unit_value.append(max_value)
        max_value_index = array.index(max_value)
        array.pop(max_value_index)
        step += 1
    return result_unit_value


# 4.3) вывести индекс минимального элемента массива
def index_min_unit(array=[10, 11, 2, 3, 5, 8, 23, 11, 2, 5, 76, 43, 2, 32, 76, 3, 10, 0, 1]):
    """Функция определяет индекс(-ы) минимального елемента массива"""
    min_value = min(array)
    # print(min_value)
    result = [index for index, unit_value in enumerate(array) if unit_value == min_value]
    return result


# 4.4) вывести исходный массив в обратном порядке
def reversed_array(array=[10, 11, 2, 3, 5, 8, 23, 11, 2, 5, 76, 43, 2, 32, 76, 3, 10, 0, 1]):
    """Функция выводит переданый ей массив в обратном порядке"""
    rev_array = [unit for unit in reversed(array)]
    return rev_array


# 5) Найти общие ключи в двух словарях:
# dict_one = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
# dict_two = {'a': 6, 'b': 7, 'z': 20, 'x': 40}


def shared_keys(dict_one={'a': 1, 'b': 2, 'c': 3, 'd': 4},
                dict_two={'a': 6, 'b': 7, 'z': 20, 'x': 40}):
    """Функция определяет общие ключи в перданых словарях"""
    keys_dict_one = {key for key, values in dict_one.items()}
    keys_dict_two = {key for key, values in dict_two.items()}
    shared_keys_in_dict = keys_dict_one.intersection(keys_dict_two)
    return shared_keys_in_dict


# 6)Дан массив из словарей
data = [
    {'name': 'Viktor', 'city': 'Kiev', 'age': 30},
    {'name': 'Maksim', 'city': 'Dnepr', 'age': 20},
    {'name': 'Vladimir', 'city': 'Lviv', 'age': 32},
    {'name': 'Andrey', 'city': 'Kiev', 'age': 34},
    {'name': 'Artem', 'city': 'Dnepr', 'age': 50},
    {'name': 'Dmitriy', 'city': 'Lviv', 'age': 21}]


# 6.1) отсортировать массив из словарей по значению ключа ‘age'
def sorted_by_age(data):
    # Функция сортирует массив словарей по значению age
    sorted_data = sorted(data, key=lambda age: age['age'])
    return sorted_data


# 6.2) сгруппировать данные по значению ключа 'city'
def group_by_city(data, sorted_key='city'):
    """Функция групперует данные по заданному ключу в заданном массиве словарей"""
    result = {}
    for unit in data:
        city = unit[sorted_key]
        if city not in result.keys():
            unit.pop(sorted_key)
            result[city] = [unit]
        elif city in result.keys():
            unit.pop(sorted_key)
            new_city_data = [*result.get(city), unit]
            result[city] = new_city_data
    return pprint.pprint(result, sort_dicts=False, width=50)


# вывод должен быть такого вида :
result = {
    'Kiev': [
        {'name': 'Viktor', 'age': 30},
        {'name': 'Andrey', 'age': 34}],

    'Dnepr': [{'name': 'Maksim', 'age': 20},
              {'name': 'Artem', 'age': 50}],
    'Lviv': [{'name': 'Vladimir', 'age': 32},
             {'name': 'Dmitriy', 'age': 21}]
}

# =======================================================
# 7) У вас есть последовательность строк. Необходимо определить наиболее часто встречающуюся строку в последовательности.
# Например:
list_var = ['a', 'a', 'bi', 'bi', 'bi']


def most_frequent(list_var):
    """Функция определяет наиболее частро встречаемую строку или строки"""
    count_elemets_list_var = Counter(list_var)
    max_value_in_count_list_var = max(count_elemets_list_var.values())
    most_frequent_elemets = [key for key, values in count_elemets_list_var.items() if
                             values == max_value_in_count_list_var]
    return '  '.join(most_frequent_elemets)


# most_frequent(['a', 'a', 'bi', 'bi', 'bi']) == 'bi'
# =======================================================
# 8) Дано целое число. Необходимо подсчитать произведение всех цифр в этом числе, за исключением нулей.
# Например:
# Дано число 123405. Результат будет: 1*2*3*4*5=120.
def multiplication_all_number(number=123405):
    """Функция реализует подстчет произведения всех чисел числа исключая ноль"""
    number_in_str = str(number)
    list_number = []
    for index_number in range(0, len(number_in_str)):
        if int(number_in_str[index_number]) == 0:
            continue
        else:
            list_number.append(int(number_in_str[index_number]))
    result = reduce(lambda x, y: x * y, list_number)
    return result


# =======================================================
# 9) Есть массив с положительными числами и число n (def some_function(array, n)).
# Необходимо найти n-ую степень элемента в массиве с индексом n. Если n за границами массива, тогда вернуть -1.
def n_degree_n_elements_in_array(array=[10, 11, 2, 3, 5, 8, 23], n=8):
    """Функция реализует нахождение n-ой степени елемента массива c индексом n """
    try:
        result = array[n] ** n
    except IndexError:
        result = -1
    return result


# =======================================================
# 10) Есть строка со словами и числами, разделенными пробелами (один пробел между словами и/или числами).
# Слова состоят только из букв. Вам нужно проверить есть ли в исходной строке три слова подряд.
# Для примера, в строке "hello 1 one two three 15 world" есть три слова подряд.
def three_words_in_line(data="hello 1 one two three 15 world"):
    """Функция определяет есть ли три слова подряд в заданой строке"""
    data_list = data.split(' ')
    counter = 0
    for unit in data_list:
        if counter == 3:
            break
        elif unit.isdigit() == False:
            counter += 1
        elif unit.isdigit() == True:
            counter = 0
    if counter < 3:
        return "String doesn't contain three words in a row"
    else:
        return 'String contain three words in a row'


if __name__ == '__main__':
    print('Задание №1')
    task_1 = dict_generations()
    print(task_1)

    print('Задание №2')
    task_2 = list_generations()
    pprint.pprint(task_2, compact=True)

    print('Задание №3')
    task_3 = change_consonants_to_vowels()
    print(task_3)

    print('Задание №4')
    task_4_1 = remove_duplicate_units()
    print(f' - 4.1 {task_4_1}')
    task_4_2 = three_max_unit()
    print(f' - 4.2 {task_4_2}')
    task_4_3 = index_min_unit()
    print(f' - 4.3 {task_4_3}')
    task_4_4 = reversed_array()
    print(f' - 4.4 {task_4_4}')

    print('Задание №5')
    task_5 = shared_keys()
    pprint.pprint(task_5, compact=True)

    print('Задание №6')
    print('- 6.1')
    task_6_1 = sorted_by_age(data)
    pprint.pprint(task_6_1, compact=True, sort_dicts=False)
    print('- 6.2')
    task_6_2 = group_by_city(data, sorted_key='city')

    print('Задание №7')
    task_7 = most_frequent(list_var)
    print(task_7)

    print('Задание №8')
    task_8 = multiplication_all_number()
    pprint.pprint(task_8)

    print('Задание №9')
    task_9_a = n_degree_n_elements_in_array(n=5)
    print(f'"n" в приделах массива данных: {task_9_a}')
    task_9_b = n_degree_n_elements_in_array(n=8)
    print(f'"n" за пределами массива данных: {task_9_b}')

    print('Задание №10')
    task_10 = three_words_in_line()
    print(task_10)
