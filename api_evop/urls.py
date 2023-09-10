from django.urls import path, include, re_path
from rest_framework import routers

from api_evop.views import AllFoodsAPIList, FoodAPIUpdate, FoodAPIDetailView, FoodsViewSet, AddIntakeAPIList

router = routers.DefaultRouter()  # + route *8000:api/
router.register(r'food', FoodsViewSet)

urlpatterns = [
    path('all-foods/', AllFoodsAPIList.as_view()),  # GET, POST, HEAD, OPTIONS
    path('food-update/<int:pk>', FoodAPIUpdate.as_view()),  # PUT, PATCH, OPTIONS;
    path('food-detail/<int:pk>', FoodAPIDetailView.as_view()),  # GET, PUT, PATCH, DELETE, HEAD, OPTIONS
    path('add-intake/', AddIntakeAPIList.as_view()),  # GET, POST, HEAD, OPTIONS
    path('', include(router.urls)),  # ViewSet --> /food-->GET, POST, HEAD, OPTIONS;
    # ViewSet --> /food-->GET, POST, HEAD, OPTIONS; /food/pk -->GET, PUT, PATCH, DELETE, HEAD, OPTIONS
    path('auth-session/', include('rest_framework.urls')),
    path('auth-token/', include('djoser.urls')),  # token-djoser
    re_path(r'^auth-token/', include('djoser.urls.authtoken')),  # token-djoser

    # path('add-food/', AddFood.as_view(), name='add_food'),
    # path('food/<int:food_id>/', show_food, name='show_food'),
    # path('intake/', AddIntake.as_view(), name='intake'),
    # path('caclulation', CalculetionResult.as_view(), name='calculation_result'),
    # path('sign-up', SignUp.as_view(), name='sign_up'),
    # path('sign-in/', SignIn.as_view(), name='sign_in'),
    # path('sign-out/', sign_out_user, name='sign_out'),
    # # path('category/<slug:cat_slug>/', cache_page(60 * 15)(ShowCategory.as_view()), name='category'),
    # path('category/<slug:cat_slug>/', ShowCategory.as_view(), name='category'),
    # path('feedback/', FeedBack.as_view(), name='feedback'),
    # path('success/<str:args>', success, name='success')

]
