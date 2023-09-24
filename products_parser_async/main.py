import asyncio

from products_parser_async.steps import get_all_categories, get_all_products
import time

all_products = []
categories = []


async def main():
    cats = asyncio.create_task(get_all_categories())
    await cats
    categories.append(cats.result())

    products = asyncio.create_task(get_all_products())
    await products
    all_products.append(products.result())


if __name__ == '__main__':
    current = time.time()
    asyncio.run(main())
    print(time.time() - current)

print(all_products)

# numb_categories = [str(num) for num in range(1, len(categories) + 1)]
# pars_category = dict(zip(categories, numb_categories))
#

# pars_category ={'Крупы': '1', 'Молочные продукты': '2', 'Яйца': '3', 'Мясо, птица': '4', 'Зелень и овощи': '5', 'Фрукты и ягоды': '6',
#  'Рыба и морепродукты': '7', 'Хлеб и хлебобулочные изделия': '8', 'Мука и мучные изделия': '9', 'Бобовые': '10',
#  'Колбаса и колбасные изделия': '11', 'Масло, маргарин, пищевые жиры': '12', 'Грибы': '13',
#  'Орехи, семена, сухофрукты': '14', 'Сладости, торты': '15', 'Икра': '16', 'Алкогольные напитки': '17',
#  'Безалкогольные напитки': '18'}

# name_category = [seafoods, vegetables_fruits_berries, butter_margarine_edible, drinks, eggs_milk_dairy,
#                  meat_sausage_products, bakery_cereals_pasta, nuts_mushrooms, confectionery_products, legumes]
# number_category = [str(num) for num in range(1, len(name_category) + 1)]
# category_products = dict(zip(number_category, name_category))
# async def main():
#     cats = asyncio.create_task(get_all_categories())
#     await cats
#
#     fish = asyncio.create_task(get_products(pars_category['Рыба и морепродукты']))
#     await fish
#     caviar = asyncio.create_task(get_products(pars_category['Икра']))
#     await caviar
#     vegetables= asyncio.create_task(get_products(pars_category['Зелень и овощи']))
#     await vegetables
#     fruit = asyncio.create_task(get_products(pars_category['Фрукты и ягоды']))
#     await fruit
#     butter_margarine_edible= asyncio.create_task(pars_category['Масло, маргарин, пищевые жиры'])
#     await butter_margarine_edible
#     drinks = asyncio.create_task(pars_category['Алкогольные напитки'])
#     await drinks
#     non_alco_drinks = asyncio.create_task(pars_category['Безалкогольные напитки'])
#     await non_alco_drinks
#     eggs = asyncio.create_task(get_products(pars_category['Яйца']))
#     await eggs
#
#     milk_dairy = asyncio.create_task(pars_category['Молочные продукты'])
#     await milk_dairy
#     meat = asyncio.create_task(get_products(pars_category['Мясо, птица']))
#     await meat
#     sausage_products  = asyncio.create_task(pars_category['Колбаса и колбасные изделия'])
#     await sausage_products
#     bakery = asyncio.create_task(get_products(pars_category['Крупы']))
#     await bakery
#     bakery2 = asyncio.create_task(pars_category['Хлеб и хлебобулочные изделия'])
#     await bakery2
#     pasta = asyncio.create_task(pars_category['Мука и мучные изделия'])
#     await pasta
#     nuts = asyncio.create_task(pars_category['Орехи, семена, сухофрукты'])
#     await nuts
#     mushrooms = asyncio.create_task(pars_category['Грибы'])
#     await mushrooms
#     confectionery_products = asyncio.create_task(pars_category['Сладости, торты'])
#     await confectionery_products
#     legumes = asyncio.create_task(pars_category['Бобовые'])
#     await legumes
#
