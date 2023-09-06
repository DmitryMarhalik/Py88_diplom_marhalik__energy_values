from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    # path('', main_page, name='home'),
    # path('', cache_page(60*60)(HomePage.as_view()), name='home'),
    path('', HomePage.as_view(), name='home'),

    path('all-foods/', cache_page(60 * 15)(AllFoods.as_view()), name='all_foods'),

    path('add-food/', AddFood.as_view(), name='add_food'),
    # path('succsess-add-food/<str:food>/', success_add_food, name='success_add_food'),
    path('food/<int:food_id>/', show_food, name='show_food'),

    path('intake/', AddIntake.as_view(), name='intake'),
    # path('succsess-add-intake/', success_add_intake, name='success_add_intake'),
    # path('add_food/', add_food, name='add_food'),
    # path('intake/', intake, name='intake'),
    path('caclulation', CalculetionResult.as_view(), name='calculation_result'),
    # path('finall_caclulation', CalculetionResult.as_view(), name='final_result'),

    path('sign-up', SignUp.as_view(), name='sign_up'),
    # path('succes_registration/<str:name>/', success_registration_user, name='success_registration_user'),

    path('sign-in/', SignIn.as_view(), name='sign_in'),
    # path('success-sign-in/<str:name>/', success_sign_in, name='sign_in_main'),
    path('sign-out/', sign_out_user, name='sign_out'),
    # path('all_foods/', all_foods, name='all_foods'),

    path('category/<slug:cat_slug>/', cache_page(60 * 15)(ShowCategory.as_view()), name='category'),
    path('feedback/', FeedBack.as_view(), name='feedback'),
    # path('success-end-message/<str:name>/', success_send_message, name='success_send_message'),
    path('success/<str:args>', success, name='success')

]
