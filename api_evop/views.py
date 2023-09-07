from rest_framework import generics

from api_evop.serializer import FoodSerializer
from app_evop.models import Food


class AllFoodsAPIList(generics.ListCreateAPIView):
    queryset = Food.objects.all().filter(be_confirmed=True)
    serializer_class = FoodSerializer


class FoodAPIUpdate(generics.UpdateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class FoodAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


