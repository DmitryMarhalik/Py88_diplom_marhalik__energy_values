import django, os
from products_parser.transformaton_data import transformation_list, delete_string_xa0xa0, transformation_evop_dishes
from products_parser.get_evop_from_site import category_products, evop_first_dishes, names_first_dishes, \
    names_second_dishes, evop_second_dishes, name_salads, evop_salads

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "energy_values.settings")
django.setup()

from app_evop.models import Food, Category


def add_products_to_db(lst, category_id):
    Food.objects.bulk_create(
        [Food(name=param[0], proteins=float(param[1]), fats=float(param[2]), carbohydrates=float(param[3]),
              kcal=float(param[4]), category_id=category_id) for param in
         transformation_list(delete_string_xa0xa0(lst))])

# add_products_to_db(legumes, 10) ----> single category add
# category= {'seafoods': '1', 'vegetables_fruits_berries': '2', 'butter_margarine_edible': '3', 'drinks':'4',
# eggs_milk_dairy': '5', 'meat_sausage_products': '6', 'bakery_cereals_pasta': '7', 'nuts_mushrooms': '8',
# 'confectionery_products': '9','legumes': '10'}


def add_dishes_to_db(dict_dishes, category_id):
    Food.objects.bulk_create([Food(name=name, proteins=float(value[1]), fats=float(value[2]),
                                   carbohydrates=float(value[3]), kcal=float(value[0]), category_id=category_id)
                              for name, value in dict_dishes.items()])


####################################################################################################################
def make_dict_dishes(names, values):
    evop = transformation_evop_dishes(values)
    dict_dishes = dict(zip(names, evop))
    return dict_dishes


for category_id, list_products in category_products.items():
    add_products_to_db(list_products, category_id)

for dishes in (make_dict_dishes(names_first_dishes, evop_first_dishes),
               make_dict_dishes(names_second_dishes, evop_second_dishes),):
    add_dishes_to_db(dishes, Category.objects.get(name='🍝 Dishes').id)

add_dishes_to_db(make_dict_dishes(name_salads, evop_salads), Category.objects.get(name='🥗 Salads').id)
###################################################################################################################
