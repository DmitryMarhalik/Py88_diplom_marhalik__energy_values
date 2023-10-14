import django, os

from products_parser.transformaton_data import transformation_list, delete_string_xa0xa0, transformation_evop_dishes

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "energy_values.settings")
django.setup()

from app_evop.models import Food


def add_products_to_db(lst, category_id):
    for value in transformation_list(delete_string_xa0xa0(lst)):
        try:
            Food.objects.create(name=value[0], proteins=float(value[1]), fats=float(value[2]),
                                carbohydrates=float(value[3]),
                                kcal=float(value[4]), category_id=category_id)
        except django.db.utils.IntegrityError:  # if name in db-->continue
            continue
        except Exception:
            return 'Failed update dishes in the database'


def add_dishes_to_db(dict_dishes, category_id):
    for name, value in dict_dishes.items():
        try:
            Food.objects.create(name=name, proteins=float(value[1]), fats=float(value[2]),
                                carbohydrates=float(value[3]), kcal=float(value[0]), category_id=category_id)
        except django.db.utils.IntegrityError:  # if name in db-->continue
            continue
        except Exception:
            return 'Failed update dishes in the database'


####################################################################################################################
def make_dict_dishes(names, values):
    evop = transformation_evop_dishes(values)
    dict_dishes = dict(zip(names, evop))
    return dict_dishes

# dict_dishes={'Борщ': ['57.7 ', '3.8  ', '2.9  ', '4.3  '],'Борщ из свежей 'капусты и картофеля по 1-110':
#                                                                                  ['36 ', '1  ', '1.1  ', '5.4  '],.}

# for category_id, list_products in category_products.items():
#     add_products_to_db(list_products, category_id)

# for dishes in (make_dict_dishes(names_first_dishes, evop_first_dishes),
#                make_dict_dishes(names_second_dishes, evop_second_dishes),):
#     add_dishes_to_db(dishes, Category.objects.get(name='🍝 Dishes').id)
#
# add_dishes_to_db(make_dict_dishes(name_salads, evop_salads), Category.objects.get(name='🥗 Salads').id)
###################################################################################################################
