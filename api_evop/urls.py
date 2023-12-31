from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api_evop.views import FoodsViewSet, AddIntakeAPIList, CalculationResult, UserKcalNorma

router = routers.DefaultRouter()  # + route *8000:api/
router.register(r'food', FoodsViewSet)

urlpatterns = [
    path('add-intake/', AddIntakeAPIList.as_view()),  # GET, POST, HEAD, OPTIONS
    path('', include(router.urls)),  # ViewSet --> /food  -->GET, POST, HEAD, OPTIONS;
    # /food/pk  -->GET, PUT, PATCH, DELETE, HEAD, OPTIONS
    path('auth-session/', include('rest_framework.urls')),  # /login /logout
    path('auth-token/', include('djoser.urls')),  # token-djoser http://127.0.0.1:8000/api/auth-token/users/--registr
    re_path(r'^auth-token/', include('djoser.urls.authtoken')),  # token-djoser:  token/login, token/logout
    path('jwt-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # create jwt-token
    path('jwt-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt-token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('calculation-intakes/', CalculationResult.as_view(), name='calc_intakes'),
    path('calculation-norm-kcal/', UserKcalNorma.as_view(), name='calc_norma_kcal'),
]
