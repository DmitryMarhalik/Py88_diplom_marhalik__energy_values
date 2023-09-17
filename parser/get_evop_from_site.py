import requests

from lxml import html

root_url = 'https://bodymaster.ru/food/tablitsa-kalorijnosti-produktov'


def get_all_categories():
    response = requests.get(root_url)
    html_tree = html.fromstring(response.text)
    cats = html_tree.xpath('//div[@class="content clearfix"]/h3[position()>1]/text()')
    return cats


def get_products_from_category(cats_number):
    response = requests.get(root_url)
    html_tree = html.fromstring(response.text)
    text_request = f'//table[@class="bordered with-header"][{cats_number}]/tbody/tr[position()>1]/td/p/text()'
    products = html_tree.xpath(text_request)
    return products


cats = get_all_categories()
number_categories = [str(num) for num in range(1, len(cats) + 1)]
category = dict(zip(cats, number_categories))

seafoods = get_products_from_category(category['Рыба и морепродукты']) + get_products_from_category(
    category['Икра'])
vegetables_fruits_berries = get_products_from_category(category['Зелень и овощи']) + get_products_from_category(
    category['Фрукты и ягоды'])
drinks = get_products_from_category(category['Алкогольные напитки']) + get_products_from_category(
    category['Безалкогольные напитки'])
eggs_milk_dairy = get_products_from_category(category['Яйца']) + get_products_from_category(
    category['Молочные продукты'])
butter_margarine_edible = get_products_from_category(category['Масло, маргарин, пищевые жиры'])
meat_sausage_products = get_products_from_category(category['Мясо, птица']) + get_products_from_category(
    category['Колбаса и колбасные изделия'])
bakery_cereals_pasta = get_products_from_category(category['Крупы']) + get_products_from_category(
    category['Хлеб и хлебобулочные изделия']) + get_products_from_category(category['Мука и мучные изделия'])
nuts_mushrooms = get_products_from_category(category['Грибы']) + get_products_from_category(
    category['Орехи, семена, сухофрукты'])
confectionery_products = get_products_from_category(category['Сладости, торты'])
legumes = get_products_from_category(category['Орехи, семена, сухофрукты'])


# {'Крупы': '1', 'Молочные продукты': '2', 'Яйца': '3', 'Мясо, птица': '4', 'Зелень и овощи': '5', 'Фрукты и ягоды': '6',
#  'Рыба и морепродукты': '7', 'Хлеб и хлебобулочные изделия': '8', 'Мука и мучные изделия': '9', 'Бобовые': '10',
#  'Колбаса и колбасные изделия': '11', 'Масло, маргарин, пищевые жиры': '12', 'Грибы': '13',
#  'Орехи, семена, сухофрукты': '14', 'Сладости, торты': '15', 'Икра': '16', 'Алкогольные напитки': '17',
#  'Безалкогольные напитки': '18'}

# //div[@class="blog-ul"]/h3 ---категория
# //div[@class="blog-ul"]/table/tbody/tr[position()>1 and position()<last()]/td/text() ---prod

# //div[@class="content clearfix"]/h3[position()>1 and position()<last()]/text() ---cat
# //table[@class="bordered with-header"]/tbody/tr[position()>1 and position()<last()]/td/p/text()
