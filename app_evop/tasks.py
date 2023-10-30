from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from celery import shared_task

from app_evop.models import Category
from products_parser.add_to_db import add_products_to_db, add_dishes_to_db
from products_parser.get_evop_from_site import products_by_category, evop_first_dishes, names_first_dishes, \
    names_second_dishes, evop_second_dishes, name_salads, evop_salads
from products_parser.transformaton_data import make_dict_dishes


@shared_task()
def send_email_task(user_email, message):
    """
    Sends an email when the feedback or add-food form has been submitted.
    """
    try:
        send_mail('EVOP app',
                  message=message,
                  from_email=user_email,
                  recipient_list=[settings.EMAIL_HOST_USER],
                  )
    except BadHeaderError:
        return HttpResponse('Incorrect header found')
        # BadHeaderError, чтобы предотвратить вставку злоумышленниками дополнительных заголовков электронной почты.
        # Если обнаружен “плохой заголовок”, то представление вернет клиенту HttpResponse с текстом
        # “Incorrect header found”.


@shared_task()
def update_products_in_the_db():
    added_products = []
    for category_id, list_products in products_by_category.items():
        new_products = add_products_to_db(list_products, category_id)
        if new_products:
            added_products.extend(new_products)
    return added_products


@shared_task()
def update_dishes_in_the_db():
    added_dishes = (add_dishes_to_db(make_dict_dishes(names_first_dishes, evop_first_dishes),
                                     Category.objects.get(name='🍝 Dishes').id) +
                    add_dishes_to_db(make_dict_dishes(names_second_dishes, evop_second_dishes),
                                     Category.objects.get(name='🍝 Dishes').id) +
                    add_dishes_to_db(make_dict_dishes(name_salads, evop_salads),
                                     Category.objects.get(name='🥗 Salads').id))
    return added_dishes
