import os
import re
import string


# 1)Из текстового файла удалить все слова, содержащие от трех до пяти символов, но при этом из каждой строки
# должно быть удалено только четное количество таких слов.
def open_file(sourse_file_name):
    # sourse_file_path = os.path.dirname(os.path.abspath(sourse_file_name))
    sourse_file_path = os.path.abspath(sourse_file_name)
    print(sourse_file_path)
    with open(sourse_file_path, 'r', encoding="UTF8") as file:
        file_string = file.readlines()
    return file_string


def write_file(sourse_file_name, result_string):
    result_file_name = (sourse_file_name.split('.'))[0] + '_result.txt'
    dirname_sourse_file = os.path.dirname(os.path.abspath(sourse_file_name))
    result_file_path = os.path.join(dirname_sourse_file, result_file_name)
    with open(result_file_path, 'a', encoding="UTF8", newline='\n') as file:
        file.write(result_string)


def remove_words_by_condition(sourse_file_name="task_1_text.txt"):
    source_data = open_file(sourse_file_name)
    for string in source_data:
        list_string = string.split()
        remove_words = check_one_string(list_string)
        if not remove_words:
            write_file(sourse_file_name,string)



def check_string_len(string):
    if 3 <= len(string) <= 5:
        return True
    return False


def check_one_string(list_string):
    remove_words_list = []
    template_punctuation = "[" + f"{string.punctuation}" + "]"
    template_сyrillic = "[А-Яа-яЁё]"
    for unit_string in list_string:
        if re.findall(r'\d', unit_string):
            continue
        elif re.findall(template_punctuation, unit_string) is not False:
            new_unit_string = ''.join(re.findall(template_сyrillic, unit_string))
            if check_string_len(new_unit_string):
                remove_words_list.append(new_unit_string)
        elif check_string_len(unit_string):
            remove_words_list.append(unit_string)
    print(remove_words_list)
    if not remove_words_list or len(remove_words_list) == 1:
        return False
    if not len(remove_words_list) % 2 == 0:
        remove_words_list.pop(-1)
    return remove_words_list


# 2)Текстовый файл содержит записи о телефонах и их владельцах. Переписать в другой файл телефоны
# тех владельцев, фамилии которых начинаются с букв К и С.


# 3) Получить файл, в котором текст выровнен по правому краю путем равномерного добавления пробелов.


# 4)Дан текстовый файл со статистикой посещения сайта за неделю. Каждая строка содержит ip адрес, время и название
# дня недели (например, 139.18.150.126 23:12:44 sunday). Создайте новый текстовый файл, который бы содержал список ip
# без повторений из первого файла. Для каждого ip укажите количество посещений, наиболее популярный день недели.
# Последней строкой в файле добавьте наиболее популярный отрезок времени в сутках длиной один час в целом для

if __name__ == '__main__':
    print("Task #1")
    result = remove_words_by_condition()
    print(result)
