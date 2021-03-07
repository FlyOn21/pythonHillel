import json
import os
import shutil
import time
from pprint import pprint
from typing import NoReturn, List, Dict, Union, Tuple


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


class DatabaseOpenCloseMixin():
    """Mixin class created for reading, writing and backup of an impromptu database"""

    def _backup_database(self) -> NoReturn:
        try:
            backup_file_path = os.path.abspath("shopDataBaseBackup.json")
            shutil.copyfile(os.path.abspath("shopDataBase.json"), backup_file_path)
        except FileNotFoundError:
            raise FileNotFoundError("Database is not found")

    def json_load(self) -> NoReturn:
        try:
            with open(os.path.abspath("shopDataBase.json"), 'r', encoding='UTF-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("Database is not found")
        except json.JSONDecodeError:
            return shutil.copyfile(os.path.abspath("shopDataBaseBackup.json"), os.path.abspath("shopDataBase.json"))

    def json_dump(self, data: dict) -> NoReturn:
        self._backup_database()
        try:
            with open(os.path.join(os.path.abspath("shopDataBase.json")), 'w', encoding='UTF-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            shutil.copyfile(os.path.abspath("shopDataBaseBackup.json"), os.path.abspath("shopDataBase.json"))
            raise json.JSONDecodeError("Error occurred while writing to the database, no data was entered")


class ShopWarehouse(DatabaseOpenCloseMixin):
    """Сlass implements work with goods in the store's warehouse"""

    class PriceDescriptor():
        """Descriptor class for creating prices in the database including NDS"""

        def __get__(self, instance, owner):
            return instance._price

        def __set__(self, instance, value):
            if value is None:
                raise ValueError("Price is always defined")
            new_price_value = value * 1.2
            instance._price = new_price_value

    price = PriceDescriptor()

    def __init__(self):
        self._all_data = self.json_load()  # contains all database
        self._warehouse_data = self._all_data["warehouse"]  # warehouse data

    def add_products(self, name: str, description: str, quantity: int, price: float, availability: int = 0,
                     category: str = "Other") -> NoReturn:
        """Add products in database"""
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

    def delete_products(self, name: str) -> NoReturn:
        """Delete products from database"""
        try:
            self._warehouse_data.pop(name)
            self._all_data["warehouse"] = self._warehouse_data
            self.json_dump(data=self._all_data)
        except KeyError:
            pass

    def product_balans(self, name: str) -> str:
        """Method returns the number of items in stock by item name"""
        try:
            product_quantity = self._warehouse_data[name]["quantity"]
            return f"The {name} in stock {product_quantity}"
        except KeyError:
            return "There is no such item in stock"

    def all_products_quantity(self) -> List[str]:
        """All products list quantity returns """
        all_products = []
        for name, values in self._warehouse_data.items():
            product_quantity = self._warehouse_data[name]["quantity"]
            all_products.append(f"{name} = {product_quantity}")
        return all_products

    def category_items(self, category_name: str) -> str:
        """Returns a list of all products for a given category"""
        category_items_list = []
        for product_name, product_data in self._warehouse_data.items():
            for param_key, param_value in product_data.items():
                if param_value == category_name:
                    category_items_list.append(product_name)
        return f"{category_name} category list product {category_items_list}"


class CustomerBasket(DatabaseOpenCloseMixin):
    """Сlass implements work with a shopping baskets"""

    def __init__(self, customer_id):
        self._all_database = self.json_load()
        self._customer_id = str(customer_id)  # basket owner id

    def add_products_in_basket(self, product_name: str, units_quantity: int = 1):
        """Add products in customer basket"""
        customer_basket = self._open_customer_basket()
        new_basket = self._check_add_in_basket(product_name, units_quantity, customer_basket)
        if not isinstance(new_basket, tuple):
            self._all_database["baskets"][self._customer_id] = new_basket
            self.json_dump(data=self._all_database)
            return
        print(new_basket[1])

    def _open_customer_basket(self) -> Dict:
        """Checks if the user has a basket or creates a new one"""
        if self._customer_id in self._all_database["baskets"]:
            basket = self._all_database["baskets"][self._customer_id]
            return basket
        return {"items": {}, "total_price": 0}

    def _check_add_in_basket(self, product_name: str, units_quantity: int, basket: Dict) -> Union[
        Tuple[bool, str], bool]:
        """Pre-check when adding an item to the basket"""
        try:
            warehouse_unit = self._all_database["warehouse"][product_name]  # find curent product in database
        except KeyError:
            return (False, "Product not found")
        if warehouse_unit["availability"]:  # checking flag availability product
            units_price = warehouse_unit["price"]  # unit price according to the database
            try:
                if basket["items"][product_name]:  # checks if the given item is already in the basket
                    units_quantity_current = basket["items"][product_name][
                        "units_quantity"]  # current product quantity in basket
                    new_units_quantity = units_quantity_current + units_quantity  # new product quantity in basket
                    checking_quantity = self._check_quantity(warehouse_unit,
                                                             new_units_quantity)  # checking if it is available
                    # to order a new quantity of goods. The check returns True or a tuple consisting of at index 0 False,
                    # at index 1 explaining why the check failed
                    if not isinstance(checking_quantity, tuple):  #
                        basket["items"][product_name] = {"units_quantity": new_units_quantity,
                                                         "units_price": round((units_price * new_units_quantity), 3)}
                    else:
                        return checking_quantity
            except KeyError:  # If the added product is not yet in the basket, then an KeyError will occur,
                # which we intercept and create a new record
                checking_quantity = self._check_quantity(warehouse_unit, units_quantity)
                if not isinstance(checking_quantity, tuple):
                    basket["items"][product_name] = {"units_quantity": units_quantity,
                                                     "units_price": round((units_price * units_quantity), 3)}
                else:
                    return checking_quantity
            basket["total_price"] = 0  # dump total price to zero
            for product, product_basket_data in basket["items"].items():  # calculate the total price of the basket
                basket["total_price"] = round((basket["total_price"] + product_basket_data["units_price"]), 3)
            return basket
        return (False, "Product not availability")

    def _check_quantity(self, warehouse_unit: Dict, units_quantity: int) -> Union[Tuple[bool, str], bool]:
        """Checking if there is enough product in warehouse"""
        if warehouse_unit["quantity"] < units_quantity:
            quantity = warehouse_unit["quantity"]
            description = warehouse_unit["description"]
            return (False, f"There are not enough units of the product {description}, currently available {quantity}")
        return True

    def basket_overview(self) -> str:
        """Returns the text presentation of customer basket"""
        basket = self._open_customer_basket()
        products = basket["items"]
        total_price = basket["total_price"]
        return f"Products {products} | total price {total_price}"

    def _clear_basket(self) -> NoReturn:
        """Сlears the user's cart if the item changes its status to ordered"""
        try:
            self._all_database["baskets"].pop(self._customer_id)
            self.json_dump(data=self._all_database)
        except KeyError:
            pass


class CustomerOrder(CustomerBasket, DatabaseOpenCloseMixin):
    """Сlass works with user orders"""

    def __init__(self, customer_id):
        super().__init__(CustomerBasket)
        self._customer_id = str(customer_id)

    def place_an_order(self):
        """Function implements the order confirmation process"""
        try:
            order = self._all_database["baskets"][self._customer_id]  # take customer basket statement
            change_quantity = self._change_quantity_in_warehouse(order)  # change product quantity in warehouse
            if not isinstance(change_quantity, tuple):
                order["customer_id"] = self._customer_id
                order["date_purchased"] = time.ctime()
                order["order_id"] = self._order_id()
                self._all_database["orders"][self._order_id()] = order  # add order in database
                self._clear_basket()  # basket that went into the order is cleared
                self.json_dump(data=self._all_database)
                return
            return change_quantity[1]
        except KeyError:
            return (False, "User's basket is empty")

    def print_order_details(self, order_id:int) -> str:
        """Print order details"""
        try:
            order = self._all_database["orders"][str(order_id)]
            pprint(order)
        except KeyError:
            print("There is no order with this number")

    def _order_id(self) -> int:
        """Take order id number"""
        all_orders = self._all_database["orders"]
        last_order = len(all_orders)
        order_id = last_order + 1
        return order_id

    def _change_quantity_in_warehouse(self, order: Dict) -> Union[Tuple[bool, str], bool]:
        warehouse = self._all_database["warehouse"]
        sold_item = self._sold_item(order)  # a dictionary is returned where the key is the name of the product,
        # the value is the quantity of the product sold
        for sold_item_name, sold_quantity in sold_item.items():
            if sold_item_name in warehouse:
                old_units_quantity = warehouse[sold_item_name]["quantity"]  # quantity in stock before sale
                new_units_quantity = old_units_quantity - sold_quantity  # quantity in stock after sale
                if new_units_quantity < 0:  # action if the goods are not enough for sale
                    warehouse[sold_item_name]["quantity"] = 0
                    warehouse[sold_item_name]["availability"] = 0
                    return (False, f"Product {sold_item_name} is out of stock or there "
                                   f"is no required quantity of the product. In stock {old_units_quantity}")
                elif new_units_quantity == 0:  # action if product out of stock
                    warehouse[sold_item_name]["availability"] = 0
                warehouse[sold_item_name]["quantity"] = new_units_quantity
        self.json_dump(data=self._all_database)
        return True

    def _sold_item(self, order: Dict) -> Dict[str, int]:
        """We get the goods that the buyer wants to buy and how much"""
        sold_item = {}
        items = order["items"]
        for product_name, basket_data in items.items():
            for key, values in basket_data.items():
                if key == "units_quantity":
                    sold_item[product_name] = values
        return sold_item


if __name__ == "__main__":
    unit_one = ShopWarehouse()
    unit_one.add_products("Качели","Крылатые качели", 3,25.0)
    unit_one.delete_products("Окно")
    print(unit_one.product_balans("Пенофол"))
    pprint(unit_one.all_products_quantity())
    print(unit_one.category_items("Other"))

    unit_second = CustomerBasket(customer_id=1)
    unit_second.add_products_in_basket("Пеноблоки", 12)
    unit_second.add_products_in_basket("Кирпич", 6)
    unit_second.add_products_in_basket("Плита", 10)
    unit_second.add_products_in_basket("Плита", 1)
    print(unit_second.basket_overview())
    unit_second.add_products_in_basket("Руберойд", 92)

    unit_third = CustomerOrder(2)
    print(unit_third.place_an_order())
    unit_third.print_order_details(2)
