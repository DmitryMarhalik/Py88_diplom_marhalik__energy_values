from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm

from app_evop.models import Food, Intake, User


class AddFoodForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'category not selected'

    class Meta:
        model = Food
        fields = ['name', 'bar_code', 'proteins', 'fats', 'carbohydrates', 'kcal', 'category', 'image']


class IntakeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['food'].empty_label = 'select dishes or product'
        self.fields['food'].queryset = Food.objects.all().filter(be_confirmed=True)

    class Meta:
        model = Intake
        fields = ['food', 'gram']


class RegisterUserForm(UserCreationForm):
    # username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'})}


class FeedbackForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    email = forms.EmailField(label='Email')
    content = forms.CharField(label='Content', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()


class CalculationResultForm(forms.Form):
    days = forms.IntegerField(label='Enter the number of days here', min_value=1)


class CalculationIndividualKcalForm(forms.Form):
    choices = (("MIN", "minimal"),
               ("WEAK", "weak"),
               ("MID", "middle"),
               ("HEAVY", "heavy"),
               ("EXTR", "extreme"),)

    gender=forms.ChoiceField(choices=(('Male', 'male'),('Female','female'),))
    height = forms.IntegerField(label='Your height in cm', min_value=10)
    weight = forms.IntegerField(label='Your weight in kg', min_value=20)
    age = forms.IntegerField(label='Your full years', min_value=20)
    activity = forms.ChoiceField(label='Choose your physical activity', choices=choices)
