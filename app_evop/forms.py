from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm

from app_evop.models import Food, Intake, User
from app_evop.tasks import send_email_task


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

    def send_email(self):
        user_email = self.cleaned_data.get('email')
        name = self.cleaned_data.get('name')
        content = self.cleaned_data.get('content')
        message = f'name: {name}\nemail: {user_email}\nmessage: {content}'
        send_email_task.delay(user_email, message)
        # send_feedback_email_task.apply_async(args=[user_email,message])
# Вызов .delay() — это самый быстрый способ отправить сообщение о задаче в Celery. Этот метод является ярлыком для
# более мощного метода .apply_async(), который дополнительно поддерживает параметры выполнения для точной настройки
# вашего сообщения о задаче.


class CalculationResultForm(forms.Form):
    days = forms.IntegerField(label='Enter the number of days here', min_value=1)


class CalculationIndividualKcalForm(forms.Form):
    choices = (("MIN", "minimal"),
               ("WEAK", "weak"),
               ("MID", "middle"),
               ("HEAVY", "heavy"),
               ("EXTR", "extreme"),)

    gender = forms.ChoiceField(label='gender', choices=(('MALE', 'Male'), ('FEMALE', 'Female'),))
    height = forms.IntegerField(label='height (cm)', min_value=10)
    weight = forms.IntegerField(label='weight (kg)', min_value=20)
    age = forms.IntegerField(label='full years', min_value=20)
    activity = forms.ChoiceField(label='activity', choices=choices)
