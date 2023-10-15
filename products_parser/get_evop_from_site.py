import requests

from lxml import html

from products_parser.setting import root_products_url, root_second_dishes, root_first_dishes, xpath_name_first_dishes, \
    xpath_categories, xpath_name_second_dishes, xpath_evop_second_dishes, xpath_evop_first_dishes, root_salads, \
    xpath_salads_name, xpath_evop_salads


def get_html_elements(text, xpath_request):
    return html.fromstring(text).xpath(xpath_request)


def get_all_categories():
    response = requests.get(root_products_url)
    categories = get_html_elements(response.text, xpath_categories)
    return categories


def get_products_from_category(cats_number):
    response = requests.get(root_products_url)
    products = get_html_elements(response.text,
                                 f'//table[@class="bordered with-header"][{cats_number}]/'
                                 f'tbody/tr[position()>1]/td/p/text()[1]')
    return products


#
cats = get_all_categories()
numb_categories = [str(num) for num in range(1, len(cats) + 1)]
pars_category = dict(zip(cats, numb_categories))
# pars_category = {'Крупы': '1', 'Молочные продукты': '2', 'Яйца': '3', 'Мясо, птица': '4', 'Зелень и овощи': '5',
#  'Фрукты и ягоды': '6','Рыба и морепродукты': '7', 'Хлеб и хлебобулочные изделия': '8', 'Мука и мучные изделия': '9',
#  'Бобовые': '10','Колбаса и колбасные изделия': '11', 'Масло, маргарин, пищевые жиры': '12', 'Грибы': '13',
#  'Орехи, семена, сухофрукты': '14', 'Сладости, торты': '15', 'Икра': '16', 'Алкогольные напитки': '17',
#  'Безалкогольные напитки': '18'}


seafoods = get_products_from_category(pars_category['Рыба и морепродукты']) + get_products_from_category(
    pars_category['Икра'])
vegetables_fruits_berries = get_products_from_category(pars_category['Зелень и овощи']) + get_products_from_category(
    pars_category['Фрукты и ягоды'])
butter_margarine_edible = get_products_from_category(pars_category['Масло, маргарин, пищевые жиры'])
drinks = get_products_from_category(pars_category['Алкогольные напитки']) + get_products_from_category(
    pars_category['Безалкогольные напитки'])
eggs_milk_dairy = get_products_from_category(pars_category['Яйца']) + get_products_from_category(
    pars_category['Молочные продукты'])
meat_sausage_products = get_products_from_category(pars_category['Мясо, птица']) + get_products_from_category(
    pars_category['Колбаса и колбасные изделия'])
bakery_cereals_pasta = get_products_from_category(pars_category['Крупы']) + get_products_from_category(
    pars_category['Хлеб и хлебобулочные изделия']) + get_products_from_category(pars_category['Мука и мучные изделия'])
nuts_mushrooms = get_products_from_category(pars_category['Грибы']) + get_products_from_category(
    pars_category['Орехи, семена, сухофрукты'])
confectionery_products = get_products_from_category(pars_category['Сладости, торты'])
legumes = get_products_from_category(pars_category['Бобовые'])

name_category = [seafoods, vegetables_fruits_berries, butter_margarine_edible, drinks, eggs_milk_dairy,
                 meat_sausage_products, bakery_cereals_pasta, nuts_mushrooms, confectionery_products, legumes]
number_category = [str(num) for num in range(1, len(name_category) + 1)]
products_by_category = dict(zip(number_category, name_category))


# ##################################################################################################################
def get_dishes(url, xpath_name, xpath_evop):
    response = requests.get(url)
    name_dish = get_html_elements(response.text, xpath_name)
    evop_dish = get_html_elements(response.text, xpath_evop)
    return name_dish, evop_dish


names_first_dishes, evop_first_dishes = get_dishes(root_first_dishes, xpath_name_first_dishes, xpath_evop_first_dishes)
names_second_dishes, evop_second_dishes = get_dishes(root_second_dishes, xpath_name_second_dishes,
                                                     xpath_evop_second_dishes)
name_salads, evop_salads = get_dishes(root_salads, xpath_salads_name, xpath_evop_salads)

# name_salads=['Винегрет', 'Винегрет из овощей', 'Винегрет из овощей и фруктов','Винегрет из овощей, яблок и зелени',..]
# evop_salads=['130,1 кКал', '1,7 г', '10,3 г', '8,2 г', '176,9 кКал', '1,9 г', '13,9 г', '11,7 г', '137,4 кКал',...]
