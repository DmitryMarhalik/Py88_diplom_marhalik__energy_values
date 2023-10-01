from rest_framework import serializers

from app_evop.models import Food, Intake


class FoodSerializer(serializers.ModelSerializer):
    bar_code = serializers.CharField(max_length=14, default=None)  # for default = null

    class Meta:
        model = Food
        # fields = '__all__'
        fields = ('name', 'bar_code', 'proteins', 'fats', 'carbohydrates', 'kcal', 'category', 'image')


class IntakeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Intake
        fields = ('food', 'gram', 'user', 'time')


class DaysSerializer(serializers.Serializer):
    days = serializers.IntegerField(label='Enter the number of days here', min_value=1)
