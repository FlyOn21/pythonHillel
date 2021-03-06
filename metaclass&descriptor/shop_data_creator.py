import random
import shop_emulator

product_name_category = {
    "Гидроизоляция и утеплители": ["Гидростеклоизол", "Глимс ВодоStop", "Изовер", "Пенополистирол",
                                   "Пенофол", "Пергамин", "Руберойд РКП-350"],
    "Гипсовые изделия, ЖБИ, кирпич": ["Бетон11", "ГКЛ влагост", "Кирпич М-100", "Пеноблоки 100 мм",
                                      "Кирпич М-150", "Плита пазогребневая обычн", "Пеноблоки 75 мм",
                                      "Плита пазогребневая влагостойкая"],
    "Other": ["Свеча", "Ручка", "Светильник", "Дверь", "Окно", ]}


def fake_database_creator(product_name_category):
    add_products = shop_emulator.ShopWarehouse()
    for category, list_products in product_name_category.items():
        print(category, list_products)
        for products in list_products:
            name = (products.split())[0]
            description = products
            quantity = random.choice(range(0, 100))
            availability = random.choice((0, 1))
            price = random.choice(range(1, 2500)) / random.choice(range(1, 50))
            add_products.add_products(name=name, description=description, quantity=quantity, price=price,
                                      availability=availability, category=category)


if __name__ == "__main__":
    fake_database_creator(product_name_category)
