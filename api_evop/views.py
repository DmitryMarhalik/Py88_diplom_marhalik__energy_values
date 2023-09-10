from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from api_evop.permissions import OnlyPostAuthUser
from api_evop.serializer import FoodSerializer, IntakeSerializer
from app_evop.models import Food, Intake, Category


# ----------------------------------------------------------------
class FoodsViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    @action(methods=['get'], detail=True)  # foods/pk(cats)/category
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
    permission_classes = (IsAuthenticated,) #(OnlyPostAythUser)
