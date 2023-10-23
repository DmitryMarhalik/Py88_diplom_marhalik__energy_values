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


class UserKcalNormaSerializer(serializers.Serializer):
    choices = (("MIN", "minimal"),
               ("WEAK", "weak"),
               ("MID", "middle"),
               ("HEAVY", "heavy"),
               ("EXTR", "extreme"),)

    gender = serializers.ChoiceField(label='gender', choices=(('MALE', 'Male'), ('FEMALE', 'Female'),))
    weight = serializers.IntegerField(label='weight (kg)', min_value=20)
    height = serializers.IntegerField(label='height (cm)', min_value=10)
    age = serializers.IntegerField(label='full years', min_value=20)
    activity = serializers.ChoiceField(label='activity', choices=choices)
