import django, os

from products_parser.transformaton_data import transformation_list, delete_string_xa0xa0, transformation_evop_lst_dishes

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "energy_values.settings")
django.setup()

from app_evop.models import Food

def add_products_to_db(lst, category_id):
    added_products = []
    for value in transformation_list(delete_string_xa0xa0(lst)):
        try:
            Food.objects.create(name=value[0], proteins=float(value[1]), fats=float(value[2]),
                                carbohydrates=float(value[3]),
                                kcal=float(value[4]), category_id=category_id)
            added_products.append(value + [f'category:{category_id}'])
        except django.db.utils.IntegrityError:  # if name in db-->continue
            continue
        except Exception:
            print('Failed update products in the database')
    return added_products


def add_dishes_to_db(dict_dishes, category_id):
    added_dishes = []
    for name, value in dict_dishes.items():
        try:
            Food.objects.create(name=name, proteins=float(value[1]), fats=float(value[2]),
                                carbohydrates=float(value[3]), kcal=float(value[0]), category_id=category_id)
            added_dishes.append([name]+value + [f'category:{category_id}'])
        except django.db.utils.IntegrityError:
            continue
        except Exception:
            print('Failed update dishes in the database')
    return added_dishes