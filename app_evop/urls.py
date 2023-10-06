from django.urls import path

# from django.views.decorators.cache import cache_page

from app_evop.views import (HomePage, AddFood, AddIntake, AllFoods, CalculetionResult, UserKcalNorma, SignUp, SignIn,
                            ShowCategory, FeedBack, show_food, sign_out_user, SendEmail)

urlpatterns = [
    # path('', cache_page(60*60)(HomePage.as_view()), name='home'),
    path('', HomePage.as_view(), name='home'),
    # path('all-foods/', cache_page(60 * 15)(AllFoods.as_view()), name='all_foods'),
    path('all-foods/', AllFoods.as_view(), name='all_foods'),
    path('add-food/', AddFood.as_view(), name='add_food'),
    path('food/<int:food_id>/', show_food, name='show_food'),
    path('intake/', AddIntake.as_view(), name='intake'),
    path('caclulation/', CalculetionResult.as_view(), name='calculation_result'),
    path('caclulation_kcal/', UserKcalNorma.as_view(), name='calculation_norma_kcal'),
    path('sign-up/', SignUp.as_view(), name='sign_up'),
    path('sign-in/', SignIn.as_view(), name='sign_in'),
    path('sign-out/', sign_out_user, name='sign_out'),
    # path('category/<slug:cat_slug>/', cache_page(60 * 15)(ShowCategory.as_view()), name='category'),
    path('category/<slug:cat_slug>/', ShowCategory.as_view(), name='category'),
    path('feedback/', FeedBack.as_view(), name='feedback'),
    path('success_send_message/',SendEmail.as_view(), name='send_email'),
]
