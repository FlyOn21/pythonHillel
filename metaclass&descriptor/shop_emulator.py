import json
import os
import shutil

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
from pprint import pprint


class PriceDescriptor():
    def __get__(self, instance, owner):
        return instance._price

    def __set__(self, instance, value):
        if value is None:
            raise ValueError("Price is always defined")
        new_price_value = value * 1.2
        instance._price = new_price_value


class DatabaseOpenCloseMixin():

    def backup_database(self, ):
        try:
            backup_file_path = os.path.abspath("shopDataBaseBackup.json")
            shutil.copyfile(os.path.abspath("shopDataBase.json"), backup_file_path)
        except FileNotFoundError:
            raise FileNotFoundError("Database is not found")

    def json_load(self):
        try:
            with open(os.path.abspath("shopDataBase.json"), 'r', encoding='UTF-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("Database is not found")
        except json.JSONDecodeError:
            self.json_dump(data={"warehouse": {}, "baskets": {}, "orders": {}})
            return self.json_load()

    def json_dump(self, data):
        self.backup_database()
        try:
            with open(os.path.join(os.path.abspath("shopDataBase.json")), 'w',
                      encoding='UTF-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            shutil.copyfile(os.path.abspath("shopDataBaseBackup.json"), os.path.abspath("shopDataBase.json"))
            raise json.JSONDecodeError("Error occurred while writing to the database, no data was entered")


class ShopWarehouse(DatabaseOpenCloseMixin):
    price = PriceDescriptor()

    def __init__(self):
        self._all_data = self.json_load()
        self._warehouse_data = self._all_data["warehouse"]

    def add_products(self, name, description, quantity, price, availability=0, category="Other"):
        self._price = price
        self._warehouse_data[name] = {
            "description": description,
            "quantity": quantity,
            "availability": availability,
            "price": round(self._price, 3),
            "category": category
        }
        self._all_data["warehouse"] = self._warehouse_data
        self.json_dump(data=self._all_data)

    def delete_products(self, name):
        try:
            self._warehouse_data.pop(name)
            self._all_data["warehouse"] = self._warehouse_data
            self.json_dump(data=self._all_data)
        except KeyError:
            pass

    def product_balanse(self, name):
        try:
            product_quantity = self._warehouse_data[name]["quantity"]
            return f"The {name} in stock {product_quantity}"
        except KeyError:
            return "There is no such item in stock"

    def all_products_quantity(self):
        all_products = []
        for name, values in self._warehouse_data.items():
            product_quantity = self._warehouse_data[name]["quantity"]
            all_products.append(f"{name} = {product_quantity}")
        return all_products

    def category_items(self, category_name):
        category_items_dict = []
        for product_name, product_data in self._warehouse_data.items():
            for param_key, param_value in product_data.items():
                if param_value == category_name:
                    category_items_dict.append(product_name)
        return f"{category_name} category list product {category_items_dict}"


class CustomerBasket(DatabaseOpenCloseMixin):

    def __init__(self):
        self._all_database = self.json_load()

    def add_products_in_basket(self, product_name, customer_id, units_quantity=1):
        customer_basket = self._open_customer_basket(customer_id)
        new_basket = self._check_basket(product_name,units_quantity,customer_basket)
        if new_basket:
            self._all_database["baskets"][self._customer_id] = new_basket
            self.json_dump(data=self._all_database)

    def _open_customer_basket(self, customer_id):
        self._customer_id = str(customer_id)
        if self._customer_id in self._all_database["baskets"]:
            basket = self._all_database["baskets"][self._customer_id]
            return basket
        return {"products": {}, "total_price": 0}


    def _check_basket(self, product_name, units_quantity, basket):
        try:
            warehouse_unit = self._all_database["warehouse"][product_name]
        except KeyError:
            return "Product not found"
        if warehouse_unit["availability"]:
            units_price = warehouse_unit["price"]
            try:
                if basket["products"][product_name]:
                    units_quantity_advance = basket["products"][product_name]["units_quantity"]
                    new_units_quantity = units_quantity_advance + units_quantity
                    checking_quantity = self._check_quantity(warehouse_unit, units_quantity)
                    if checking_quantity:
                        basket["products"][product_name] = {"units_quantity": new_units_quantity,
                                                            "units_price": round((units_price * new_units_quantity), 3)}
                    else:
                        return checking_quantity
            except KeyError:
                checking_quantity = self._check_quantity(warehouse_unit,units_quantity)
                if checking_quantity:
                    basket["products"][product_name] = {"units_quantity": checking_quantity,
                                                "units_price": round((units_price * checking_quantity), 3)}
                else:
                    return checking_quantity
            basket["total_price"] = 0
            for product, product_basket_data in basket["products"].items():
                basket["total_price"] = basket["total_price"]+product_basket_data["units_price"]
            return basket
        return False

    def _check_quantity(self,warehouse_unit,units_quantity):
        if warehouse_unit["quantity"] < units_quantity:
            quantity = warehouse_unit["quantity"]
            return f"There are not enough units of the product, currently available {quantity}"
        return True

    def basket_overview(self, customer_id):
        basket = self._open_customer_basket(customer_id)
        products = basket["products"]
        total_price = basket["total_price"]
        return f"Products {products} | total price {total_price}"

# class CustomerOrder(DatabaseOpenCloseMixin):



if __name__ == "__main__":
    unit = ShopWarehouse()
    # unit.add_products("Качели","Крылатые качели", 3,25.0)
    unit.delete_products("Окно")
    print(unit.product_balanse("Пенофол"))
    # pprint(unit.all_products_quantity())
    print(unit.category_items("Other"))
    unit_second = CustomerBasket()
    unit_second.add_products_in_basket("Пеноблоки", 1, 5)
    unit_second.add_products_in_basket("Свеча", 2, 6)
    unit_second.add_products_in_basket("Плита", 2, 3)
    unit_second.add_products_in_basket("Плита", 2, 4)
    # print(unit_second.basket_overview(1))
    # unit_second.add_products_in_basket("Плита", 3, 19)
