from typing import List, Dict, Union, Tuple, NoReturn
import json
import os
import shutil
import re
import string
from hw_class.exception import NotJSONFileTransferredError
import time


# Задача-1
# У вас есть список(list) IP адрессов. Вам необходимо создать
# класс который будет иметь методы:
# 1) Получить список IP адресов
# 2) Получить список IP адресов в развернутом виде
# (10.11.12.13 -> 13.12.11.10)
# 3) Получить список IP адресов без первых октетов
# (10.11.12.13 -> 11.12.13)
# 4) Получить список последних октетов IP адресов
# (10.11.12.13 -> 13)


class IpChangeMaker():
    def __init__(self, ip: List[str]):
        self._ip = ip

    def list_ip(self):
        return self._ip

    def list_ip_reverse(self):
        list_ip_reverse = ['.'.join(reversed(ip_unit.split("."))) for ip_unit in self._ip]
        return list_ip_reverse

    def ip_without_first_octet(self):
        list_ip_without_first_octet = ['.'.join(ip_unit.split(".")[1:]) for ip_unit in self._ip]
        return list_ip_without_first_octet

    def last_octet_ip(self):
        list_last_octet_ip = [ip_unit.split(".")[-1] for ip_unit in self._ip]
        return list_last_octet_ip


# Задача-2
# У вас несколько JSON файлов. В каждом из этих файлов есть
# произвольная структура данных. Вам необходимо написать
# класс который будет описывать работу с этими файлами, а
# именно:
# 1) Запись в файл
# 2) Чтение из файла
# 3) Объединение данных из файлов в новый файл
# 4) Получить путь относительный путь к файлу
# 5) Получить абсолютный путь к файлу
class JsonFileHandler():
    def __init__(self, *file_names_json: str):
        json_files_dict = {number: file_name for number, file_name in enumerate(file_names_json, 1)}
        try:
            for key in range(1, (len(json_files_dict) + 1)):
                if ((json_files_dict[key]).split("."))[-1] != "json":
                    raise NotJSONFileTransferredError(
                        "The class accepts only json files, the passed values of the class arguments are not json")
        except AttributeError:
            raise NotJSONFileTransferredError(
                "Сlass accepts only attribute values as a string that contains the json file name")
        self.__json_file_dict = json_files_dict

    @property
    def json_file_dict(self):
        """Returns the value of the private attribute of the class"""
        return self.__json_file_dict

    def __int_to_list(self, number_files):
        """Checks the data that came to the input of the class method and converts it"""
        if isinstance(number_files, int):
            number_files = [number_files]
            return number_files
        return number_files

    def __json_dump(self, path, write_value):
        """Writing data to a file in the format json"""
        with open(path, mode="w", encoding="UTF8") as file:
            json.dump(write_value, file, indent=2)

    def __json_load(self, file_path):
        """Reading data to a file in the format json"""
        try:
            with open(file_path, mode="r", encoding="UTF8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("File not found, check for file existence")

    def files_abspath(self, number_files: Union[int, List[int], Tuple[int, ...]]) -> List[str]:  # I connected type
        # hints so that the user understands that the public method of the class is waiting for
        # input and in order to understand this topic.
        """Method takes the numbers of the files passed to the class as arguments and returns a
        list of absolute file paths"""
        check_number_files = self.__int_to_list(number_files)
        list_file_abspath = [os.path.abspath(self.__json_file_dict[number_file])
                             for number_file in check_number_files]
        return list_file_abspath

    def files_relpath(self, number_files: Union[int, List[int], Tuple[int, ...]]) -> List[str]:
        """Method takes the numbers of the files passed to the class as
        arguments and returns a list of relative file paths"""
        check_number_files = self.__int_to_list(number_files)
        list_file_relpath = [os.path.relpath(self.__json_file_dict[number_file], start=os.pardir)
                             for number_file in check_number_files]
        return list_file_relpath

    def json_read_file(self, number_files: Union[int, List[int], Tuple[int, ...]]) -> List[Dict]:
        """Method takes the numbers of the files passed to the class as arguments and
        returns a list of data in the form of a dictionary contained in the source json files"""
        result_read_file_list = []
        file_paths = self.files_abspath(number_files)
        for file_path in file_paths:
            data = self.__json_load(file_path)
            result_read_file_list.append(data)
        return result_read_file_list

    def __copy_file_to_write_(self, files_numbers_to_write):
        """Method copies the original and creates a dictionary in which the key is the path to the copy of
        the file, and the value is the contents of the file"""
        result_path_data_dict = {}
        list_copy_file_path = []
        check_files_numbers_to_write = self.__int_to_list(files_numbers_to_write)
        list_copy_file_data = self.json_read_file(files_numbers_to_write)
        try:
            for file_number_to_write in check_files_numbers_to_write:
                new_file_name = (self.__json_file_dict[file_number_to_write].split("."))[0] + \
                                f"_recorded_{files_numbers_to_write}.json"
                dir_name_copy_file = os.path.dirname(os.path.abspath(self.__json_file_dict[file_number_to_write]))
                copy_file_path = os.path.join(dir_name_copy_file, new_file_name)
                shutil.copyfile(self.__json_file_dict[file_number_to_write], copy_file_path)
                list_copy_file_path.append(copy_file_path)
            for index in range(len(check_files_numbers_to_write)):
                result_path_data_dict[list_copy_file_path[index]] = list_copy_file_data[index]
            return result_path_data_dict
        except IOError:
            raise IOError("Error copying files for writing, check if the files exist")

    def __change_dict(self, change_dict, write_unit):
        """Method supplements the dictionary passed to the input with data for writing to it"""
        for new_key, new_value in write_unit.items():
            if new_key in change_dict.keys():
                change_dict[new_key + "|" + str(time.ctime())] = new_value
                continue
            change_dict[new_key] = new_value
        return change_dict

    def __create_new_data(self, dict_k_pathfile_v_datafile, write_data):
        """Method receives a dictionary as input where the key is the path to the file and the value is the
         file content and the data dictionary or a list of data dictionaries to write to
         the value of the original dictionary."""
        dict_changed_data_copy_file = {}
        for path_from_dict_k_pathfile_v_datafile in dict_k_pathfile_v_datafile:
            change_dict = dict_k_pathfile_v_datafile[path_from_dict_k_pathfile_v_datafile]
            if isinstance(write_data, list or tuple):
                for write_unit in write_data:
                    changed_dict = self.__change_dict(change_dict, write_unit)
                    dict_changed_data_copy_file[path_from_dict_k_pathfile_v_datafile] = changed_dict
            else:
                changed_dict = self.__change_dict(change_dict, write_data)
                dict_changed_data_copy_file[path_from_dict_k_pathfile_v_datafile] = changed_dict
        return dict_changed_data_copy_file

    def json_write_file(self, files_numbers_to_write: Union[int, List[int], Tuple[int, ...]],
                        write_data: Union[Dict, List[Dict], Tuple[Dict, ...]]) -> NoReturn:
        """Method receives as input the json file numbers or json file number passed to the class as arguments
        and data to write to them."""
        dict_k_pathfile_v_datafile = self.__copy_file_to_write_(files_numbers_to_write)
        new_data = self.__create_new_data(dict_k_pathfile_v_datafile, write_data)
        for path_from_dict_k_pathfile_v_datafile, new_value in new_data.items():
            self.__json_dump(path_from_dict_k_pathfile_v_datafile, new_value)

    def json_file_compound(self, files_numbers_to_compound: Union[int, List[int], Tuple[int, ...]], ) -> NoReturn:
        """Method combines several files into one according to the file numbers passed to the checkout as arguments"""
        compound_file_data = self.json_read_file(files_numbers_to_compound)
        result_file_name = f"compound_json_data_file{files_numbers_to_compound}{time.ctime()}.json"
        dir_name_source_file = os.path.dirname(self.files_abspath(1)[0])
        result_file_path = os.path.join(dir_name_source_file, result_file_name)
        for unit_compound_file_data in compound_file_data:
            if os.path.isfile(result_file_path):
                data = self.__json_load(result_file_path)
                new_data = self.__change_dict(data, unit_compound_file_data)
                self.__json_dump(result_file_path, new_data)
                continue
            self.__json_dump(result_file_path, unit_compound_file_data)


# Задача-3
#
# Создайте класс который будет хранить параметры для
# подключения к физическому юниту(например switch). В своем
# списке атрибутов он должен иметь минимальный набор
# (unit_name, mac_address, ip_address, login, password).
# Вы должны описать каждый из этих атрибутов в виде гетеров и
# сеттеров(@property). У вас должна быть возможность
# получения и назначения этих атрибутов в классе.

class SwitchConnectionParameters():
    def __init__(self, ):
        self.__unit_name = "switch_flyon21"
        self.__mac_address = "00:26:57:00:1f:02"
        self.__ip_address = "192.168.12.45"
        self.__login = "pasha"
        self.__password = "qwerty123!"

    @property
    def unit_name(self):
        return self.__unit_name

    @unit_name.setter
    def unit_name(self, unit_name):
        if isinstance(unit_name, str):
            self.__unit_name = unit_name
        self.__unit_name = str(unit_name)

    @property
    def mac_address(self):
        return self.__mac_address

    @mac_address.setter
    def mac_address(self, mac_address):
        check = self.__check_mac_address(mac_address)
        if check:
            self.__mac_address = mac_address

    def __check_mac_address(self, mac_address):
        """Validation of a mac_address according to requirements"""
        check_mac_address = mac_address.split(':')
        punctuation = f"[{string.punctuation}]"
        if len(check_mac_address) != 6:
            print("MAC-address is not correct")
            return False
        for mac_address_unit in check_mac_address:
            if re.findall(punctuation, mac_address_unit):
                print("MAC-address is not correct")
                return False
            if len(mac_address_unit) != 2:
                print("MAC-address is not correct")
                return False
        return True

    @property
    def ip_address(self):
        return self.__ip_address

    @ip_address.setter
    def ip_address(self, ip_address):
        if self.__check_ip_address(ip_address):
            self.__ip_address = ip_address

    def __check_ip_address(self, ip_address):
        """Validation of a ip_address according to requirements"""
        check_ip_address = ip_address.split('.')
        template = f"[{string.punctuation}]|\w\D"
        if len(check_ip_address) != 4:
            print("IP address is not correct")
            return False
        for unit_ip_address in check_ip_address:
            if re.findall(template, unit_ip_address):
                print("IP address is not correct")
                return False
            if len(unit_ip_address) > 3 or len(unit_ip_address) < 1:
                print("IP address is not correct")
                return False
        return True

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, new_login):
        self.__login = new_login

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, new_password):
        check_new_pass = self.__check_password(new_password)
        if check_new_pass:
            self.__password = new_password

    def __check_password(self, new_password):
        """Validation of a new_password according to requirements"""
        if len(new_password) < 8:
            print("New password less than 8 characters contain letters, numbers and special symbols")
            return False
        char = re.findall(r"\D\w", new_password)
        digit = re.findall(r"\d", new_password)
        punctuation = re.findall(r"[!#$%&()*+-/:;<=>?@[\]^_`{|}~]", new_password)
        if char and digit and punctuation:
            return True
        print("New password less than 8 characters contain letters, numbers and special symbols")
        return False


if __name__ == "__main__":
    print("Task_1")
    ip = ["213.27.152.15", "190.93.176.11", "37.59.115.136", "89.191.131.243", "190.117.115.150", "5.197.231.174",
          "180.247.131.229"]
    unit_one = IpChangeMaker(ip)
    print(unit_one.list_ip())
    print(unit_one.list_ip_reverse())
    print(unit_one.ip_without_first_octet())
    print(unit_one.last_octet_ip())

    print("Task_2")
    unit_second = JsonFileHandler("example_json_1.json", "example_json_2.json")
    print(unit_second.json_file_dict)
    read_data = unit_second.json_read_file((1, 2))
    unit_second.json_file_compound([1, 2])
    unit_second.json_write_file((1, 2), read_data)
    print(unit_second.files_abspath([1, 2]))
    print(unit_second.files_relpath([1, 2]))

    print("Task_3")
    unit_third = SwitchConnectionParameters()
    print(unit_third.unit_name)
    unit_third.unit_name = "lol"
    print(unit_third.unit_name)
    print(unit_third.mac_address)
    unit_third.mac_address = "48:d5:37:33:fc:20"
    print(unit_third.mac_address)
    print(unit_third.ip_address)
    unit_third.ip_address = "22.00.2.22"
    print(unit_third.ip_address)
    print(unit_third.password)
    unit_third.password = "ghkg123"
    print(unit_third.password)
