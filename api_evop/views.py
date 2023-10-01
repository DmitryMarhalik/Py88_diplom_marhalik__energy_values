from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.views import extend_schema
from drf_spectacular.utils import extend_schema_view

from api_evop.permissions import OnlyPostAuthUser,IsAdminOrReadOnly
from api_evop.serializer import FoodSerializer, IntakeSerializer, DaysSerializer
from app_evop.models import Food, Intake

from app_evop.calculation_user_tasks import intakes_between_days


class AllFoodsAPIListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'  # for get request in browser adrres
    max_page_size = 1000


# ----------------------------------------------------------------

@extend_schema_view(
    retrieve=extend_schema(
        summary="Viewing a food by id"),

    list=extend_schema(
        summary="View all products to all users",
    ),
    update=extend_schema(
        summary="Update an existing food",
    ),
    create=extend_schema(
        summary="Add a product only for registered users",
    ),
    destroy=extend_schema(
        summary="Delete an existing product only administrator",
    ),
    partial_update=extend_schema(
        summary="For a partial resource update food",
    ),
)
class FoodsViewSet(viewsets.ModelViewSet):
    """Here it is possible to perform the following actions:\n
    /food --> GET, POST, HEAD, OPTIONS.\n
    /food/pk --> GET, PUT, PATCH, DELETE, HEAD, OPTIONS.\n
    /foods/pk(category_id)/category. \n
    POST, PUT, PATCH, DELETE - For admin only!"""

    queryset = Food.objects.all().filter(be_confirmed=True)
    serializer_class = FoodSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = AllFoodsAPIListPagination

    @extend_schema(summary="Viewing foods by id categories")
    @action(methods=['get'], detail=True)  # foods/pk(category_id)/category
    def category(self, request, pk=None):
        if request.user.is_authenticated:
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


# @extend_schema_view(
#     put=extend_schema(
#         summary="Update an existing food",
#     ),
#     patch=extend_schema(
#         summary="For a partial resource update food",
#     ), )
# class FoodAPIUpdate(generics.UpdateAPIView):
#     """PUT - updating the entire object, PATCH - updating the field of the object,
#     you can also use the PUT method to update one field, but the PUT method will go
#     through all the fields of the object and look for what is needed, unlike PATCH,
#     which does not bypass the entire object"""
#     queryset = Food.objects.all()
#     serializer_class = FoodSerializer
#     permission_classes = (IsAdminUser,)

#
# class FoodAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Food.objects.all()
#     serializer_class = FoodSerializer
#     permission_classes = (IsAdminUser,)


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
    """Viewing and calculating the consumption of products"""
    serializer_class = DaysSerializer

    @extend_schema(summary="View all the user's product consumptions")
    def get(self, request):
        return Response({f'Hello,{request.user.username}!'})

    @extend_schema(summary="Here the user enters the number of days to calculate the result")
    def post(self, request):
        days = request.data['days']
        energy_values, count_of_products, message = intakes_between_days(request, days)
        if not count_of_products:
            return Response(f'You have not consumed anything for a given period of time.')
        result = {'energy_values': energy_values,
                  'count_product': count_of_products,
                  }
        return Response({f'result for {request.user.username}': result})
