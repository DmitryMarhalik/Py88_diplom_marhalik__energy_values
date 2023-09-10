from rest_framework import serializers

from app_evop.models import Food, Intake


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'
        # fields = ('name','image','bar_code','proteins','fats','carbohydrates','kcal','category')


class IntakeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Intake
        fields = ('food', 'gram', 'user', 'time')
