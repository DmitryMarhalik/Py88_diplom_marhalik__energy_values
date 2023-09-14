import requests


from lxml import html
from app_evop.models import Food


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


categories = get_all_categories()
number_categories = [str(num) for num in range(1, len(categories) + 1)]
categories_with_nums = dict(zip(categories, number_categories))


seafoods = get_products_from_category(7) + get_products_from_category(16)
vegetables_fruits_berries = get_products_from_category(5) + get_products_from_category(6)
drinks = get_products_from_category(17) + get_products_from_category(18)
eggs_milk_dairy = get_products_from_category(2) + get_products_from_category(3)
butter_margarine_edible = get_products_from_category(12)
meat_sausage_products = get_products_from_category(4) + get_products_from_category(11)
bakery_cereals_pasta = get_products_from_category(1) + get_products_from_category(8) + get_products_from_category(9)
nuts_mushrooms = get_products_from_category(13) + get_products_from_category(14)
confectionery_products = get_products_from_category(15)
legumes = get_products_from_category(10)
print(legumes)
# other = get_products_from_category()
# print(nuts_mushrooms)
# {'Крупы': '1', 'Молочные продукты': '2', 'Яйца': '3', 'Мясо, птица': '4', 'Зелень и овощи': '5', 'Фрукты и ягоды': '6',
#  'Рыба и морепродукты': '7', 'Хлеб и хлебобулочные изделия': '8', 'Мука и мучные изделия': '9', 'Бобовые': '10',
#  'Колбаса и колбасные изделия': '11', 'Масло, маргарин, пищевые жиры': '12', 'Грибы': '13',
#  'Орехи, семена, сухофрукты': '14', 'Сладости, торты': '15', 'Икра': '16', 'Алкогольные напитки': '17',
#  'Безалкогольные напитки': '18'}

# //div[@class="blog-ul"]/h3 ---категория
# //div[@class="blog-ul"]/table/tbody/tr[position()>1 and position()<last()]/td/text() ---prod

# //div[@class="content clearfix"]/h3[position()>1 and position()<last()]/text() ---cat
# //table[@class="bordered with-header"]/tbody/tr[position()>1 and position()<last()]/td/p/text()
#'Горох зерно', '20,5', '2', '49,5', '298'
# f=Food()
