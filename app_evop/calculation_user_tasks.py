from collections import Counter
from datetime import timedelta
from django.utils import timezone

from app_evop.models import Intake


def intakes_between_days(request, days):
    days_ago = timezone.now() - timedelta(days=int(days))
    all_intake_products = Intake.objects.values('food__name', 'food__proteins', 'food__fats', 'food__carbohydrates',
                                                'food__kcal', 'gram').filter(user_id=request.user.id,
                                                                             time__gte=days_ago)
    message = None
    if not all_intake_products:
        message = 'You have not consumed anything for a given period of time.'
        return None, None, message
    else:
        count_of_product = dict(
            Counter(all_intake_products.values_list('food__name')))  # {('chips',): 1,('water',):1}
        count_of_products = dict(
            sorted({k[0]: v for k, v in count_of_product.items()}.items()))  # {'chips': 1, 'water': 1}
        proteins, fats, carbohydrates, kcal, gram = 0, 0, 0, 0, 0
        for energy_value_product in all_intake_products:
            proteins += float(energy_value_product['food__proteins']) * (float(energy_value_product['gram'] / 100))
            fats += float(energy_value_product['food__fats']) * (float(energy_value_product['gram'] / 100))
            carbohydrates += float(energy_value_product['food__carbohydrates']) * (
                float(energy_value_product['gram'] / 100))
            kcal += float(energy_value_product['food__kcal']) * (float(energy_value_product['gram'] / 100))
        total_energy_values = {'proteins': round(proteins, 1), 'fats': round(fats, 1),
                               'carbohydrates': round(carbohydrates, 1), 'kcal': round(kcal, 1)}
        return total_energy_values, count_of_products, message


def calculate_norma_kcal(height,weight,age,activity):
    pass