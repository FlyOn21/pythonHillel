import os
import re
import string

# 1)Из текстового файла удалить все слова, содержащие от трех до пяти символов, но при этом из каждой строки
# должно быть удалено только четное количество таких слов.
import sys


def open_file(source_file_name):
    try:
        source_file_path = os.path.abspath(f"tasks_file_string/{source_file_name}")
        with open(source_file_path, 'r', encoding="UTF8") as file:
            list_file_string = file.readlines()
        return list_file_string
    except FileNotFoundError:
        raise FileNotFoundError("Сheck the existence of an open file or the correct"
                                " name of the file passed to the function")


def write_file(result_file_path, result_string):
    with open(result_file_path, 'a', encoding="UTF8", newline='\n') as file:
        file.write(result_string)


def check_result_file(source_file_name):
    result_file_name = (source_file_name.split('.'))[0] + '_result.txt'
    dirname_source_file = os.path.dirname(os.path.abspath(f"tasks_file_string/{source_file_name}"))
    result_file_path = os.path.join(dirname_source_file, result_file_name)
    if os.path.isfile(result_file_path):
        os.remove(result_file_path)
    return result_file_path


def check_one_string(list_string):
    remove_words_list = []
    template_punctuation = "[" + f"{string.punctuation}" + "]"
    for unit_string in list_string:
        if re.findall(r'\d', unit_string):
            continue
        elif re.findall(template_punctuation, unit_string) is not False:
            new_unit_string = ''.join(re.findall(r"[А-Яа-яЁё]|\w", unit_string))
            if check_string_len(new_unit_string):
                remove_words_list.append(new_unit_string)
        elif check_string_len(unit_string):
            remove_words_list.append(unit_string)
    if not remove_words_list or len(remove_words_list) == 1:
        return False
    if not len(remove_words_list) % 2 == 0:
        remove_words_list.pop(-1)
    return remove_words_list


def remove_words_by_condition(source_file_name="task_1_text.txt"):
    source_data = open_file(source_file_name)
    result_file_path = check_result_file(source_file_name)
    for one_string in source_data:
        list_string = one_string.split()
        remove_words = check_one_string(list_string)
        if not remove_words:
            write_file(result_file_path, one_string)
            continue
        for remove_word in remove_words:
            # print(one_string)
            find_index = one_string.find(remove_word)
            first_part_new_string = one_string[:find_index]
            second_part_new_string = one_string[(find_index + len(remove_word)):]
            one_string = first_part_new_string + second_part_new_string
            # print(one_string)
        write_file(result_file_path, one_string)
    return "File processed"


def check_string_len(string):
    if 3 <= len(string) <= 5:
        return True
    return False


# 2)Текстовый файл содержит записи о телефонах и их владельцах. Переписать в другой файл телефоны
# тех владельцев, фамилии которых начинаются с букв К и С.
def sorted_phone_book(source_file_name="task_2_phone_book.txt"):
    sorted_keys = ("к", "с")
    source_data = open_file(source_file_name)
    result_file_path_write = check_result_file(source_file_name)
    for unit_phone_note in source_data:
        prepared_unit_phone_note = unit_phone_note.lower()
        for sorted_key in sorted_keys:
            if prepared_unit_phone_note.find(sorted_key) == 0:
                write_file(result_file_path_write, unit_phone_note)
    return f"Result data sorted in file:{os.path.abspath('task_2_phone_book_result.txt')}"


# 3) Получить файл, в котором текст выровнен по правому краю путем равномерного добавления пробелов.
def right_align(source_file_name="task_3_right_align.txt", fillchar=" "):
    source_file_data = open_file(source_file_name)
    max_line_length_in_file = max((len(line) for line in source_file_data))
    result_file_path = check_result_file(source_file_name)
    for line in source_file_data:
        wight = (max_line_length_in_file - len(line)) + len(line)
        result_line = line.rjust(wight, fillchar)
        write_file(result_file_path, result_line)


# 4)Дан текстовый файл со статистикой посещения сайта за неделю. Каждая строка содержит ip адрес, время и название
# дня недели (например, 139.18.150.126 23:12:44 sunday). Создайте новый текстовый файл, который бы содержал список ip
# без повторений из первого файла. Для каждого ip укажите количество посещений, наиболее популярный день недели.
# Последней строкой в файле добавьте наиболее популярный отрезок времени в сутках длиной один час в целом для сайта.
def sorted_log_site(source_file_name = 'task_4_statistics.txt'):
    log_data = open_file(source_file_name)
    all_log_time = []
    ip_and_week_day_dict = {}
    for log_line in log_data:
        list_log_line = log_line.split('|')
        if not list_log_line[0] in ip_and_week_day_dict.keys():
            ip_and_week_day_dict[list_log_line[0]] = list_log_line[2]
        old_value = ip_and_week_day_dict[list_log_line[0]]
        new_value = [*old_value,list_log_line[2]]
        ip_and_week_day_dict[list_log_line[0]] = new_value
    print(ip_and_week_day_dict)

if __name__ == '__main__':
    print("Task #1")
    result = remove_words_by_condition()
    print(result)

    print("Task #2")
    result = sorted_phone_book()
    print(result)

    print("Task #3")
    result = right_align()

    print("Task #4")
    result_task_4 = sorted_log_site()
    print(result_task_4)
