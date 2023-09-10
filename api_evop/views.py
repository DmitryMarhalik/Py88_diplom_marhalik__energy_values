from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api_evop.permissions import OnlyPostAuthUser
from api_evop.serializer import FoodSerializer, IntakeSerializer, DaysSerializer
from app_evop.forms import CalculationResultForm
from app_evop.models import Food, Intake, Category

from app_evop.calculation_user_intakes import intakes_between_days


# ----------------------------------------------------------------
class FoodsViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    @action(methods=['get'], detail=True)  # foods/pk(category_id)/category
    def category(self, request, pk=None):
        foods = Food.objects.filter(category_id=pk)
        return Response({'foods': [food.name for food in foods]})


# ----------------------------------------------------------------
class AllFoodsAPIList(generics.ListCreateAPIView):
    queryset = Food.objects.all().filter(be_confirmed=True)
    serializer_class = FoodSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


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
    permission_classes = (OnlyPostAuthUser,)  # (IsAuthenticated,)


class CalculationResult(APIView):
    # queryset = Intake.objects.all()
    serializer_class = DaysSerializer

    # form_class = CalculationResultForm

    def get(self, request):
        return Response({'Hello'})

    def post(self, request):
        days = request.data['days']
        energy_values, count_of_products, message = intakes_between_days(request, days)
        if not count_of_products:
            return Response(f'You have not consumed anything for a given period of time.')
        result = {'energy_values': energy_values,
                  'count_product': count_of_products,
                  }
        return Response({f'result for {request.user.username}': result})
