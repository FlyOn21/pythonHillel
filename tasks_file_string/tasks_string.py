import os
import re
import string
from collections import Counter

# 1)Из текстового файла удалить все слова, содержащие от трех до пяти символов, но при этом из каждой строки
# должно быть удалено только четное количество таких слов.
import sys


def open_file(source_file_name):
    """Function open source data file"""
    try:
        source_file_path = os.path.abspath(f"tasks_file_string/{source_file_name}")
        with open(source_file_path, 'r', encoding="UTF8") as file:
            list_file_string = file.readlines()
        return list_file_string
    except FileNotFoundError:
        raise FileNotFoundError("Сheck the existence of an open file or the correct"
                                " name of the file passed to the function")


def write_file(result_file_path, result_string):
    """Function writing result function work in file"""
    with open(result_file_path, 'a', encoding="UTF8", newline='\n') as file:
        file.write(result_string)


def check_result_file(source_file_name):
    """Function generated path for save result file and checks for the presence of a file with results in the system"""
    result_file_name = (source_file_name.split('.'))[0] + '_result.txt'
    dirname_source_file = os.path.dirname(os.path.abspath(f"tasks_file_string/{source_file_name}"))
    result_file_path = os.path.join(dirname_source_file, result_file_name)
    if os.path.isfile(result_file_path):
        os.remove(result_file_path)
    return result_file_path


def check_one_line (one_line):
    """Function generating list words which deleting from transferred line"""
    list_string = one_line.split()
    remove_words_list = []
    template_punctuation = "[" + f"{string.punctuation}" + "]" # create punctuation template for regex
    for unit_string in list_string:
        if re.findall(r'\d', unit_string): # filter digits in line
            continue
        elif re.findall(template_punctuation, unit_string) is not False: #cleaning words in a line from punctuation
            new_unit_string = ''.join(re.findall(r"[А-Яа-яЁё]|\w", unit_string))
            if check_string_len(new_unit_string): # checking the length of the string according to the condition specified in the task
                remove_words_list.append(new_unit_string)
        elif check_string_len(unit_string):
            remove_words_list.append(unit_string)
    if not remove_words_list or len(remove_words_list) == 1:
        return False
    if not len(remove_words_list) % 2 == 0:
        remove_words_list.pop(-1)
    return remove_words_list


def remove_words_by_condition(source_file_name="task_1_text.txt"):
    """Main function which starts the process of checking and transforming the transferred file"""
    source_data = open_file(source_file_name)
    result_file_path = check_result_file(source_file_name)
    for one_line in source_data:
        remove_words = check_one_line (one_line)
        if not remove_words:
            write_file(result_file_path, one_line )
            continue
        for remove_word in remove_words:
            find_index = one_line .find(remove_word)
            first_part_new_string = one_line [:find_index]
            second_part_new_string = one_line [(find_index + len(remove_word)):]
            one_line = first_part_new_string + second_part_new_string
        write_file(result_file_path, one_line )
    return f"Result file:{result_file_path}"


def check_string_len(string): #moved to a single function as it is used several times
    """Сhecking a given condition in a task"""
    if 3 <= len(string) <= 5:
        return True
    return False


# 2)Текстовый файл содержит записи о телефонах и их владельцах. Переписать в другой файл телефоны
# тех владельцев, фамилии которых начинаются с букв К и С.
def sorted_phone_book(source_file_name="task_2_phone_book.txt"):
    """Function checking phone book and filter by given condition after writing the filtered data to file"""
    sorted_keys = ("к", "с")
    source_data = open_file(source_file_name)
    result_file_path_write = check_result_file(source_file_name)
    for unit_phone_note in source_data:
        prepared_unit_phone_note = unit_phone_note.lower()
        for sorted_key in sorted_keys:
            if prepared_unit_phone_note.find(sorted_key) == 0:
                write_file(result_file_path_write, unit_phone_note)
    return f"Result file:{result_file_path_write}"


# 3) Получить файл, в котором текст выровнен по правому краю путем равномерного добавления пробелов.
def right_align(source_file_name="task_3_right_align.txt", fillchar=" "):
    """Function right-aligns text fill blank space with given fill char"""
    source_file_data = open_file(source_file_name)
    max_line_length_in_file = max((len(line) for line in source_file_data))# determining the maximum line width
    result_file_path = check_result_file(source_file_name)
    for line in source_file_data:
        wight = (max_line_length_in_file - len(line)) + len(line)
        result_line = line.rjust(wight, fillchar)
        write_file(result_file_path, result_line)
    return f"Result file:{result_file_path}"

# 4)Дан текстовый файл со статистикой посещения сайта за неделю. Каждая строка содержит ip адрес, время и название
# дня недели (например, 139.18.150.126 23:12:44 sunday). Создайте новый текстовый файл, который бы содержал список ip
# без повторений из первого файла. Для каждого ip укажите количество посещений, наиболее популярный день недели.
# Последней строкой в файле добавьте наиболее популярный отрезок времени в сутках длиной один час в целом для сайта.
def creator_dict_ip_week_usage(list_log_line, popular_day_of_week):
    """Function creating dictionary where key it's ip and value it's list maximum popular days of week"""
    if not list_log_line[0] in popular_day_of_week:
        popular_day_of_week[list_log_line[0]] = [list_log_line[2].strip()]
    popular_day_of_week[list_log_line[0]] = [*(popular_day_of_week[list_log_line[0]]), list_log_line[2].strip()]
    for key, value in popular_day_of_week.items():
        counter = max(Counter(value).values()) # the largest value of the values for a specific day of the week for each unique ip
        new_value = [key for key, value in Counter(value).items() if value == counter]
        popular_day_of_week[key] = new_value
    return popular_day_of_week


def hour_max_activity(all_log_time):
    """Function determines the hour in the day with the maximum user activity on the resource"""
    activity_dict = Counter(all_log_time)
    max_popular_hour_in_day = max(activity_dict.items(), key=lambda value: value[1])
    list_define_popular_time_step_one = [unit for unit in activity_dict.items() if
                                         int(unit[0]) == int(max_popular_hour_in_day[0]) - 1
                                         or int(unit[0]) == int(max_popular_hour_in_day[0])
                                         or int(unit[0]) == int(max_popular_hour_in_day[0]) + 1]
    list_define_popular_time_step_two = sorted(list_define_popular_time_step_one,
                                               key=lambda hour_number_records: hour_number_records[1], reverse=True)
    return list_define_popular_time_step_two


def analysis_log_site(source_file_name='task_4_statistics.txt'):
    """Main function that starts the process of analyzing the log of user activity on the resource"""
    log_data = open_file(source_file_name)
    result_file_path_write = check_result_file(source_file_name)
    all_log_time = [] # list of all timestamps of user activity
    popular_days_of_week = {} # dictionary by pattern [ip]:[popular days or day of week]
    ip_usage_list = []# list of all ip which were active according to the log file
    for log_line in log_data:
        list_log_line = log_line.split('|')
        ip_usage_list.append(list_log_line[0])
        all_log_time.append(((list_log_line[1].strip()).split(":"))[0])
        creator_dict_ip_week_usage(list_log_line, popular_days_of_week)
    ip_usage_dict = Counter(ip_usage_list) # dictionary where ip it's key and the value of the number of such entries in the log file
    max_activity_on_day = hour_max_activity(all_log_time)
    creator_log_analysis_file(popular_days_of_week, ip_usage_dict, max_activity_on_day, result_file_path_write)
    # generates a template for writing to the log analysis file
    return f"Result file:{result_file_path_write}"

def creator_log_analysis_file(popular_day_of_week, ip_usage_dict, max_activity_on_day, result_file_path_write):
    """Generates a template for writing to the log analysis file"""
    for ip in popular_day_of_week:
        week_day = (str(popular_day_of_week[ip]).lstrip("[")).rstrip("]").upper()
        ip_count_in = ip_usage_dict[ip]
        result_string = f"{ip} | most popular days of activity: {week_day} | number of visits for the period: {ip_count_in}\n\n"
        write_file(result_file_path_write, result_string)
    most_popular_hour = f"Most popular times of user activity from {max_activity_on_day[1][0]} hour to {max_activity_on_day[0][0]} hour\n"
    write_file(result_file_path_write, most_popular_hour)


if __name__ == '__main__':
    print("Task #1")
    result = remove_words_by_condition()
    print(result)

    print("Task #2")
    result = sorted_phone_book()
    print(result)

    print("Task #3")
    result = right_align()
    print(result)

    print("Task #4")
    result_task_4 = analysis_log_site()
    print(result_task_4)
