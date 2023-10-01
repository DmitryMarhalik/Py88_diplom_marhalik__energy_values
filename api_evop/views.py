from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from api_evop.permissions import OnlyPostAuthUser
from api_evop.serializer import FoodSerializer, IntakeSerializer, DaysSerializer
from app_evop.models import Food, Intake

from app_evop.calculation_user_tasks import intakes_between_days


class AllFoodsAPIListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'  # for get request in browser adrres
    max_page_size = 1000


# ----------------------------------------------------------------
class FoodsViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all().filter(be_confirmed=True)
    serializer_class = FoodSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = AllFoodsAPIListPagination

    @action(methods=['get'], detail=True)  # foods/pk(category_id)/category
    def category(self, request, pk=None):
        foods = Food.objects.filter(category_id=pk)
        return Response({'foods: ([proteins], [fats], [carbohydrates], [kcal], [image])':
                             [f'{food.name}: ([{food.proteins}], [{food.fats}], [{food.carbohydrates}]; '
                              f'[{food.kcal}], [{food.image}])' for food in foods]})


# ----------------------------------------------------------------
class AllFoodsAPIListCreate(generics.ListCreateAPIView):
    queryset = Food.objects.all().filter(be_confirmed=True)
    serializer_class = FoodSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = AllFoodsAPIListPagination


class FoodAPIUpdate(generics.UpdateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = (IsAdminUser,)


class FoodAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = (IsAdminUser,)


# ----------------------------------------------------------------
class AddIntakeAPIList(generics.ListCreateAPIView):
    queryset = Intake.objects.all()
    serializer_class = IntakeSerializer
    permission_classes = (IsAuthenticated,)

    # model=Intake

    def get_queryset(self):
        # queryset = self.model.objects.filter(user_id=self.request.user.id)
        return super().get_queryset().filter(user_id=self.request.user.id)


class CalculationResult(APIView):
    serializer_class = DaysSerializer

    def get(self, request):
        return Response({f'Hello,{request.user.username}!'})

    def post(self, request):
        days = request.data['days']
        energy_values, count_of_products, message = intakes_between_days(request, days)
        if not count_of_products:
            return Response(f'You have not consumed anything for a given period of time.')
        result = {'energy_values': energy_values,
                  'count_product': count_of_products,
                  }
        return Response({f'result for {request.user.username}': result})
