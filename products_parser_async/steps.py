import aiohttp

from lxml import html

root_url = 'https://bodymaster.ru/food/tablitsa-kalorijnosti-produktov'

categories = []
products = []


# numb_categories = [str(num) for num in range(1, len(categories) + 1)]
# pars_category = dict(zip(categories, numb_categories))

# pars_category ={'Крупы': '1', 'Молочные продукты': '2', 'Яйца': '3', 'Мясо, птица': '4', 'Зелень и овощи': '5',
# 'Фрукты и ягоды': '6',
#  'Рыба и морепродукты': '7', 'Хлеб и хлебобулочные изделия': '8', 'Мука и мучные изделия': '9', 'Бобовые': '10',
#  'Колбаса и колбасные изделия': '11', 'Масло, маргарин, пищевые жиры': '12', 'Грибы': '13',
#  'Орехи, семена, сухофрукты': '14', 'Сладости, торты': '15', 'Икра': '16', 'Алкогольные напитки': '17',
#  'Безалкогольные напитки': '18'}


def get_html_elements(text, xpath_request):
    return html.fromstring(text).xpath(xpath_request)


async def get_all_categories():
    async with aiohttp.ClientSession() as session:
        async with session.get(root_url) as response:
            text = await response.text()
            cats = get_html_elements(text, '//div[@class="content clearfix"]/h3[position()>1]/text()')
            categories.extend(cats)
            return categories


async def get_all_products():
    async with aiohttp.ClientSession() as session:
        async with session.get(root_url) as response:
            text = await response.text()
            products = get_html_elements(text,
                                         f'//table[@class="bordered with-header"]/tbody/tr[position()>1]/td/p/text()[1]')
            products.extend(products)
            return products

# async def get_products(cats_number):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(root_url) as response:
#             text = await response.text()
#             products = get_html_elements(text,
#                                      f'//table[@class="bordered with-header"][{cats_number}]/tbody/tr[position()>1]/td/p/text()[1]')
#             products.extend(products)
#             return products


# seafoods = get_products_from_category(pars_category['Рыба и морепродукты']) + get_products_from_category(
#     pars_category['Икра'])
# vegetables_fruits_berries = get_products_from_category(
#     pars_category['Зелень и овощи']) + get_products_from_category(
#     pars_category['Фрукты и ягоды'])
# butter_margarine_edible = get_products_from_category(pars_category['Масло, маргарин, пищевые жиры'])
# drinks = get_products_from_category(pars_category['Алкогольные напитки']) + get_products_from_category(
#     pars_category['Безалкогольные напитки'])
# eggs_milk_dairy = get_products_from_category(pars_category['Яйца']) + get_products_from_category(
#     pars_category['Молочные продукты'])
# meat_sausage_products = get_products_from_category(pars_category['Мясо, птица']) + get_products_from_category(
#     pars_category['Колбаса и колбасные изделия'])
# bakery_cereals_pasta = get_products_from_category(pars_category['Крупы']) + get_products_from_category(
#     pars_category['Хлеб и хлебобулочные изделия']) + get_products_from_category(
#     pars_category['Мука и мучные изделия'])
# nuts_mushrooms = get_products_from_category(pars_category['Грибы']) + get_products_from_category(
#     pars_category['Орехи, семена, сухофрукты'])
# confectionery_products = get_products_from_category(pars_category['Сладости, торты'])
# legumes = get_products_from_category(pars_category['Бобовые'])


# name_category = [seafoods, vegetables_fruits_berries, butter_margarine_edible, drinks, eggs_milk_dairy,
#                  meat_sausage_products, bakery_cereals_pasta, nuts_mushrooms, confectionery_products, legumes]
# number_category = [str(num) for num in range(1, len(name_category) + 1)]
# category_products = dict(zip(number_category, name_category))
