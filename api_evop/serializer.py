from rest_framework import serializers

from app_evop.models import Food


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'
        # fields = ('name','image','bar_code','proteins','fats','carbohydrates','kcal','category')


