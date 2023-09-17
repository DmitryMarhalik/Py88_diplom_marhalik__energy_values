import django, os
from parser.transformaton_data import transformation_list
from parser.get_evop_from_site import seafoods, drinks, vegetables_fruits_berries, eggs_milk_dairy, \
    bakery_cereals_pasta, butter_margarine_edible, nuts_mushrooms, legumes, confectionery_products, \
    meat_sausage_products

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "energy_values.settings")
django.setup()

from app_evop.models import Food


def add_data_to_db(lst, category_id):
    Food.objects.bulk_create(
        [Food(name=i[0], proteins=float(i[1]), fats=float(i[2]), carbohydrates=float(i[3]), kcal=float(i[4]),
              category_id=category_id) for i in transformation_list(lst)])


add_data_to_db(seafoods, 1)
