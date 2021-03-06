import re


# Задача-1
# Реализовать дескриптор валидации для аттрибута email.
# Ваш дескриптор должен проверять формат email который вы пытаетесь назначить
class EmailValidationError(Exception):

    def __init__(self, msg="Email is not correct", status_code=12):
        self._msg = msg
        self._status_code = status_code

    def __str__(self):
        return f"{self._msg}, status code {self._status_code}"


class EmailDescriptor:
    def __get__(self, instance, owner):
        return instance._email


    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise EmailValidationError()
        if not re.findall(r"[@]", value):
            raise EmailValidationError()
        email_list = value.split("@")
        if len(email_list) > 2:
            raise EmailValidationError()
        if not re.findall(r"[.]", email_list[1]):
            raise EmailValidationError()
        instance._email = value


class MyClass:
    email = EmailDescriptor()

    def __init__(self, email=None):
        self._email = email


my_class = MyClass()
print(my_class.email)
my_class.email = "validemail@gmail.com"
print(my_class.email)
#
# my_class.email = "novalidemail"


# Raised Exception


# Задача-2
# Реализовать синглтон метакласс(класс для создания классов синглтонов).

class Singleton(type):
    _class_instances = {}

    def __call__(cls, *args, **kwargs):
        if cls in cls._class_instances:
            return cls._class_instances[cls]
        cls._class_instances[cls] = super().__call__(*args, **kwargs)
        return cls._class_instances[cls]


class MyClass(metaclass=Singleton):
    pass


c = MyClass()
b = MyClass()
print(id(c), id(b))
assert id(c) == id(b)


# Задача-3
# реализовать дескриптор IngegerField(), который будет хранить уникальные
# состояния для каждого класса где он объявлен

class IngegerField:

    def __init__(self, attr_name):
        self.attr_name = attr_name

    def __get__(self, instance, owner):
        return instance.__dict__[self.attr_name]

    def __set__(self, instance, value):
        instance.__dict__[self.attr_name] = value


class Data:
    number = IngegerField("number")


data_row = Data()
new_data_row = Data()

data_row.number = 5
print(data_row.__dict__)
new_data_row.number = 10
print(new_data_row.__dict__)

assert data_row.number != new_data_row.number

# Задача4
# Необходимо создать модели работы со складскими запасами товаров и процесса оформления заказа этих товаров.
# Cписок требований:
# 1) Создайте товар с такими свойствами, как имя(name), подробные сведения(description or details),
# количество на складе(quantity), доступность(availability), цена(price).
# 2) Добавить товар на склад
# 3) Удалить товар со склада
# 4) Распечатать остаток товара по его имени
# 5) Распечатать остаток всех товаров
# 6) Товар может принадлежать к категории
# 7) Распечатать список товаров с заданной категорией
# 8) Корзина для покупок, в которой может быть много товаров с общей ценой.
# 9) Добавить товары в корзину (вы не можете добавлять товары, если их нет в наличии)
# 10) Распечатать элементы корзины покупок с ценой и общей суммой
# 11) Оформить заказ и распечатать детали заказа по его номеру
# 12) Позиция заказа, созданная после оформления заказа пользователем.
# Он будет иметь идентификатор заказа(order_id), дату покупки(date_purchased), товары(items), количество(quantity)
# 13) После оформления заказа количество товара уменьшается на количество товаров из заказа.


# Добавить к этой задаче дескриптор для аттрибута цена.
# При назначении цены товара будет автоматически добавлен НДС 20%
# При получении цены товара, цена возврщается уже с учетом НДС
