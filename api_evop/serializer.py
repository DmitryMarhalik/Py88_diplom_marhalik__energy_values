from rest_framework import serializers

from app_evop.models import Food, Intake


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class IntakeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Intake
        fields = ('food', 'gram', 'user', 'time')

class DaysSerializer(serializers.Serializer):
    days = serializers.IntegerField(label='Enter the number of days here',min_value=1)