import ast
import copy
import json
import pytest
from shop_emulator import ShopWarehouse, PriceDescriptor, DatabaseOpenCloseMixin, CustomerBasket
import os
import shutil
import simplejson
from config_test import *


@pytest.fixture(scope="module")
def copy_base_file():
    """ Fixture backuped main database files and replaced to mock database """
    shutil.copyfile(os.path.abspath("shopDataBase.json"),
                    os.path.join(os.getcwd(), "temporary_storage_master/shopDataBase.json"))
    shutil.copyfile(os.path.abspath("shopDataBaseBackup.json"),
                    os.path.join(os.getcwd(), "temporary_storage_master/shopDataBaseBackup.json"))
    shutil.copyfile(os.path.join(os.getcwd(), "files_for_test_open_close/shopDataBaseMock.json"),
                    os.path.abspath("shopDataBase.json"))
    yield
    shutil.copyfile(os.path.join(os.getcwd(), "temporary_storage_master/shopDataBase.json"),
                    os.path.abspath("shopDataBase.json"))
    shutil.copyfile(os.path.join(os.getcwd(), "temporary_storage_master/shopDataBaseBackup.json"),
                    os.path.abspath("shopDataBaseBackup.json"))


class TestsDescriptor():
    """Test class tested description PriceDescriptor """
    class MockClass(): # created mock class with PriceDescriptor
        price = PriceDescriptor()

        def __init__(self, price):
            self.price = price

    @pytest.mark.parametrize("price,price_nds", [(15.0, 18.000), (25.0, 30.000)])
    def test_set(self, price, price_nds):
        """ test set new value in price attribute"""
        desc = PriceDescriptor()
        res = desc.__set__(desc, price)
        assert res == price_nds

    @pytest.mark.parametrize("price,price_nds", [(15.0, 18.000), (25.0, 30.000)])
    def test_get(self, price, price_nds):
        """test for getting value attribute price"""
        unit = self.MockClass(price)
        res = unit.price
        assert res == price_nds


class TestShopWarehouse():

    @pytest.fixture()
    def created_cls_obj_fake_attributes(self):
        """Fixture created object class ShopWarehouse and changes attributes value in current object """
        wh = ShopWarehouse()
        wh._all_data = TEST_WAREHOUSE_DATA
        wh._warehouse_data = TEST_WAREHOUSE_DATA["warehouse"]
        return wh

    @pytest.fixture()
    def wh_instance(self):
        """Fixture created object class ShopWarehouse """
        wh = ShopWarehouse()
        return wh

    def test_add_products(self, wh_instance,copy_base_file):
        """test function add_product in class ShopWarehouse. """
        test_result_flag = False
        wh_instance.add_products("Дверь", "Хорошая дверь", 10, 15.0, 1)
        data = wh_instance.json_load()
        for key, values in data["warehouse"].items():
            if key == list(TEST_WAREHOUSE_UNIT.keys())[0] and values == \
                    list(TEST_WAREHOUSE_UNIT.values())[0]:
                test_result_flag = True
        assert test_result_flag == True

    @pytest.mark.parametrize("name, expected_result", [("Глимс", "The Глимс in stock 84"),
                                              ("asdasdas", "There is no such item in stock")])
    def test_product_balance(self, wh_instance,copy_base_file, name, expected_result):
        """test function product_balance in class ShopWarehouse"""
        method_result = wh_instance.product_balance(name)
        assert method_result == expected_result

    @pytest.mark.parametrize("name, expected_result", [("Глимс", None),
                                              ("asdasdas", "That product not in database or it's delete")])
    def test_delete_products(self, wh_instance,copy_base_file, name, expected_result):
        """test function delete_products in class ShopWarehouse"""
        method_result = wh_instance.delete_products(name)
        assert method_result == expected_result

    def test_all_products_quantity(self, created_cls_obj_fake_attributes):
        """test function all_products_quantity in class ShopWarehouse"""
        result = created_cls_obj_fake_attributes.all_products_quantity()
        assert result == ["Гидростеклоизол = 73", "Глимс = 84", "Качели = 3"]

    @pytest.mark.parametrize("category, result_list", [("Other", ["Качели"]),
                                                       ("Гидроизоляция и утеплители", ["Гидростеклоизол", "Глимс"])])
    def test_category_items(self, created_cls_obj_fake_attributes, category, result_list):
        """test function category_items in class ShopWarehouse"""
        func_result_str = created_cls_obj_fake_attributes.category_items(category)
        index = func_result_str.find("[")
        result = func_result_str[index:]
        print(result)
        assert result == str(result_list)


class TestDatabaseOpenCloseMixin():

    @pytest.fixture(scope="class")
    def tested_class_obj(self):
        """Fixture created object class DatabaseOpenCloseMixin"""
        class_obj = DatabaseOpenCloseMixin()
        return class_obj


    def test_json_load_ok(self, copy_base_file, tested_class_obj):
        """test function json_load, when loading json file it's ok and function correct work"""
        data_test_func = tested_class_obj.json_load()
        assert type(data_test_func) == type(dict())
        with open(os.path.abspath("shopDataBase.json")) as file:
            data_to_check = simplejson.load(file)
            assert data_test_func == data_to_check

    def test_json_load_file_not_found(self, copy_base_file, tested_class_obj):
        """test json load function, when loading file is not found"""
        os.remove(os.path.abspath("shopDataBase.json"))
        with pytest.raises(FileNotFoundError) as exinfo:
            tested_class_obj.json_load()
        assert (str(exinfo.value)) == "Database is not found"

    def test_json_load_file_decode_error(self, copy_base_file, tested_class_obj):
        """test json load function, when json file isn't serialized and raised error JSONDecodeError"""
        shutil.copyfile(os.path.join(os.getcwd(), "files_for_test_open_close/shopDataBase_loud.json"),
                        os.path.abspath("shopDataBase.json"))
        data = tested_class_obj.json_load()
        assert data[0] == "Error read database"

    def test_backup_databases(self, copy_base_file, tested_class_obj):
        """test backup_databases function work is correct """
        tested_class_obj._backup_database()
        with open(os.path.abspath("shopDataBase.json"), "r") as data_master:
            with open(os.path.abspath("shopDataBaseBackup.json"), "r") as data_backup:
                assert data_master.read() == data_backup.read()

    def test_json_dump_ok(self, copy_base_file, tested_class_obj):
        """test json_dump function, when function correct work"""
        tested_class_obj.json_dump(TEST_WAREHOUSE_DATA)
        with open(os.path.abspath("shopDataBase.json"), "r") as data:
            assert ast.literal_eval(data.read()) == TEST_WAREHOUSE_DATA

    def test_json_dump_value_error(self, copy_base_file, tested_class_obj):
        """test json_dump function, when dump data is not correct format or data corrupted"""
        data = "'{'test':'velue_test'}"
        with pytest.raises(ValueError) as exinfo:
            tested_class_obj.json_dump(data)
        assert (str(exinfo.value)) == "The data transferred for recording does not meet the requirement. " \
                                      "The data must be a dictionary."


class TestCustomerBasket():

    @pytest.fixture()
    def open_mock_database(self):
        """Fixture open/close mock database json file"""
        with open(os.path.join(os.getcwd(), "files_for_test_open_close/shopDataBaseMock.json"), "r",
                  encoding="UTF8") as file:
            data = json.load(file)
            return data

    @pytest.fixture()
    def take_test_class_obj(self, open_mock_database):
        """Fixture return CustomerBasket class object """
        obj_basket = CustomerBasket(2)
        obj_basket._all_database = open_mock_database
        return obj_basket


    @pytest.fixture()
    def take_test_basket(self):
        """The fixture returns the prepared item (basket) from the test config file """
        data = copy.deepcopy(TEST_BASKET)
        return data


    @pytest.mark.parametrize("class_obj,result_basket", [(CustomerBasket(2), TEST_BASKET),
                                                         (CustomerBasket(0), {"items": {}, "total_price": 0})])
    def test_open_customer_basket(self, class_obj, result_basket):
        """test open_customer_basket in two completion options,
        when a basket exists and when a new basket is created """
        result = class_obj._open_customer_basket()
        assert result == result_basket

    @pytest.mark.parametrize("quantity, excepted_result", [(5, True),
                                                  (20, (False, f"There are not enough units of the product "
                                                               f"{TEST_WAREHOUSE_UNIT['Дверь']['description']}, "
                                                               f"currently available "
                                                               f"{TEST_WAREHOUSE_UNIT['Дверь']['quantity']}"))])
    def test_check_quantity_(self, quantity, excepted_result, take_test_class_obj):
        """test check_quantity function in two completion options, when the required quantity of goods is in warehouse
        and if the required quantity is not """
        test_result = take_test_class_obj._check_quantity(TEST_WAREHOUSE_UNIT["Дверь"], quantity)
        assert test_result == excepted_result

    def test_check_add_in_basket_product_not_found(self, take_test_class_obj, take_test_basket):
        """test check_add_in_baske function when current product not found in warehouse """
        result = take_test_class_obj._check_add_in_basket(product_name="fdsfsdfs", units_quantity=1,
                                                          basket=take_test_basket)
        assert result[0] == False
        assert result[1] == "Product not found"

    def test_check_add_in_basket_not_available(self, take_test_class_obj, take_test_basket):
        """test check_add_in_baske function when current product not available in warehouse """
        result = take_test_class_obj._check_add_in_basket(product_name="Светильник", units_quantity=1,
                                                          basket=take_test_basket)
        assert result == (False, "Product not availability")

    def test_check_add_in_basket_check_ok(self, take_test_class_obj, take_test_basket):
        """test check_add_in_basket function when current product passed all checks and can be added """
        result = take_test_class_obj._check_add_in_basket(product_name="ГКЛ", units_quantity=1,
                                                          basket=take_test_basket)
        assert result == TEST_BASKET_ADD

    @pytest.mark.parametrize("product_name, units_quantity, result_units_quantity, units_price, result_total_price",
                             [("Бетон11", 8, 8, 168.0, 2768.69), ("Ручка", 10, 10, 179.71, 2780.4),
                              ("Плита", 1, 7, 78.288, 2611.874)])
    def test_check_add_in_basket_correct_info_add(self, take_test_class_obj,take_test_basket, product_name, units_quantity,
                                                  result_units_quantity, units_price, result_total_price):
        """test check_add_in_basket function, checking correct add product values in basket"""
        basket = take_test_basket
        result = take_test_class_obj._check_add_in_basket(product_name=product_name, units_quantity=units_quantity,
                                                          basket=basket)
        assert result["items"][product_name]["units_quantity"] == result_units_quantity
        assert result["items"][product_name]["units_price"] == units_price
        assert result["total_price"] == result_total_price



    @pytest.mark.parametrize("product_name, units_quantity, expected_result", [("ГКЛ", 1, TEST_BASKET_ADD),
                                                                               ("Качели", 2,
                                                                                (False, "Product not availability"))])
    def test_add_products_in_basket(self, copy_base_file, take_test_class_obj, product_name, units_quantity,
                                    expected_result):
        """test add_products_in_basket function when current product is added to the basket and when not """
        result = take_test_class_obj.add_products_in_basket(product_name, units_quantity)
        if result == "OK":
            with open(os.path.abspath("shopDataBase.json"), "r",
                      encoding="UTF8") as file:
                data = json.load(file)
                result = data["baskets"]["2"]
        assert result == expected_result

    def test_basket_overview(self, take_test_class_obj,take_test_basket):
        """test basket_overview function, correct return string represintation"""
        expected_result = f"Products {take_test_basket['items']} | total price {take_test_basket['total_price']}"
        result = take_test_class_obj.basket_overview()
        assert result == expected_result


    def test_clear_basket(self, copy_base_file, take_test_class_obj,take_test_basket):
        """test clear_basket function, The correctness of the function is checked by an attempt to request a remote
        basket object and the occurrence of a Key Error as a result """
        take_test_class_obj._clear_basket()
        with pytest.raises(KeyError):
            with open(os.path.abspath("shopDataBase.json"), "r",
                      encoding="UTF8") as file:
                data = json.load(file)
                return data["baskets"]["2"]