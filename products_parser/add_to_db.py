import django, os
from products_parser.transformaton_data import transformation_list, delete_string_xa0xa0
from products_parser.get_evop_from_site import category_products

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "energy_values.settings")
django.setup()

from app_evop.models import Food


def add_data_to_db(lst, category_id):
    Food.objects.bulk_create(
        [Food(name=param[0], proteins=float(param[1]), fats=float(param[2]), carbohydrates=float(param[3]),
              kcal=float(param[4]), category_id=category_id) for param in
         transformation_list(delete_string_xa0xa0(lst))])


# add_data_to_db(legumes, 10)
for category_id, list_products in category_products.items():
    add_data_to_db(list_products, category_id)

# category= {'seafoods': '1', 'vegetables_fruits_berries': '2', 'butter_margarine_edible': '3', 'drinks':'4',
# eggs_milk_dairy': '5', 'meat_sausage_products': '6', 'bakery_cereals_pasta': '7', 'nuts_mushrooms': '8',
# 'confectionery_products': '9','legumes': '10'}
