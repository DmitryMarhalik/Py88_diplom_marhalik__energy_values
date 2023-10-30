from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView
from django.views.generic.base import TemplateView

from app_evop.forms import IntakeForm, AddFoodForm, CalculationResultForm, RegisterUserForm, FeedbackForm, \
    CalculationIndividualKcalForm
from app_evop.models import Food
from app_evop.utils import ContextMixin
from app_evop.calculation_user_tasks import get_values_between_days, get_individual_norm_kcal
from app_evop.tasks import send_email_task


class HomePage(ContextMixin, ListView):
    model = Food  # if not ---> HomePage is missing a QuerySet. Define HomePage.model,
    # HomePage.queryset, or override HomePage.get_queryset().
    template_name = 'evop/main.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Main page')
        context.update(user_context)
        return context


class AllFoods(ContextMixin, ListView):
    paginate_by = 16
    model = Food
    template_name = 'evop/all_foods.html'
    context_object_name = 'foods'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='All foods', cat_selected='all_foods')
        context.update(user_context)
        return context

    def get_queryset(self):
        return Food.objects.filter(be_confirmed=True)


class AddFood(ContextMixin, CreateView):
    form_class = AddFoodForm
    template_name = 'evop/add_food.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Add food')
        context.update(user_context)
        return context

    def form_valid(self, form):
        context = self.get_user_context()
        food = form.cleaned_data.get('name')
        bar_code = form.cleaned_data.get('bar_code')
        proteins = form.cleaned_data.get('proteins')
        fats = form.cleaned_data.get('fats')
        carbohydrates = form.cleaned_data.get('carbohydrates')
        kcal = form.cleaned_data.get('kcal')
        category = form.cleaned_data.get('category')
        text_message = (f'food: {food}\nbar_code: {bar_code}\nproteins: {proteins}'
                        f'\nfats: {fats}\ncarbohydrates: {carbohydrates}\nkcal: {kcal}\ncategory: {category}')
        message = (f'name: {self.request.user.username}\nemail: {self.request.user.email}\n'
                   f'the proposed product:\n{text_message}')
        form.save()
        send_email_task.delay(self.request.user.email, message)  # celery
        return render(self.request, 'evop/successful_action.html', {'tabs': context['tabs'],
                                                                    'categories': context['categories'], 'food': food})


class ShowCategory(ContextMixin, ListView):
    paginate_by = 16
    template_name = 'evop/show_category.html'
    context_object_name = 'foods'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Category : ' + str(context['foods'][0].category.name),
                                             cat_selected=context['foods'][0].category.slug)
        context.update(user_context)
        return context

    def get_queryset(self):
        cat_slug = self.kwargs['cat_slug']  # c.get_absolute_url(basis)--(!!get_abs_url.models.kwargs!!)
        return Food.objects.filter(category__slug=cat_slug, be_confirmed=True).order_by('name')


class AddIntake(ContextMixin, CreateView):
    form_class = IntakeForm
    template_name = 'evop/intake.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Intake')
        context.update(user_context)
        return context

    def form_valid(self, form):
        context = self.get_user_context()
        form.instance.user_id = self.request.user.id
        form.save()
        food = form.cleaned_data.get('food')
        return render(self.request, 'evop/successful_action.html', {'tabs': context['tabs'],
                                                                    'title': 'Intake added',
                                                                    'categories': context['categories'],
                                                                    'intake': food})


class UserKcalNorma(ContextMixin, FormView):
    template_name = 'evop/individual_kcal_norm.html'
    form_class = CalculationIndividualKcalForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Individual norm kcal')
        context.update(user_context)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_user_context()
        gender = request.POST.get('gender')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        age = request.POST.get('age')
        activity = request.POST.get('activity')
        user_norm_kcal = get_individual_norm_kcal(gender, float(height), float(weight), float(age), activity)
        context = {'tabs': context['tabs'], 'categories': context['categories'],
                   'title': f'{request.user.username} norma kcal ',
                   'user_kcal': user_norm_kcal, 'user_name': request.user.username
                   }
        return render(request, 'evop/final_result_kcal.html', context=context)


class CalculetionIntakes(ContextMixin, FormView):
    template_name = 'evop/calculation_intakes.html'
    form_class = CalculationResultForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Calculation intakes')
        context.update(user_context)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_user_context()
        days = request.POST.get('days')
        energy_values, count_of_products, message = get_values_between_days(request, days)
        context = {'tabs': context['tabs'], 'categories': context['categories'],
                   'title': 'Final calculation',
                   'energy_values': energy_values,
                   'count_product': count_of_products, 'message': message, 'name': request.user.username
                   }
        if not count_of_products:
            context['title'] = 'No result'
        return render(request, 'evop/final_result_intake.html', context=context)


class FeedBack(ContextMixin, FormView):
    form_class = FeedbackForm
    template_name = 'evop/feedback.html'
    success_url = reverse_lazy('successful_send_email')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Feedback')
        context.update(user_context)
        return context

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class SendEmail(ContextMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        context = self.get_user_context(title='Send message')
        context = {'tabs': context['tabs'], 'categories': context['categories'],
                   'feedbackname': request.user.username
                   }
        return render(request, 'evop/successful_action.html', context=context)


class SignIn(ContextMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'evop/sign_in.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Sign In')
        context.update(user_context)
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('home')


class SignUp(ContextMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'evop/sign_up.html'
    success_url = reverse_lazy('sign_in')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Sign Up')
        context.update(user_context)
        return context

    # def form_valid(self, form):        #для автоматического входа при регистрации
    #     user=form.save()
    #     login(self.request, user)
    #     return redirect('home')


def sign_out_user(request):
    logout(request)
    return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>404 --> Page Not Found 😔</h1>')


def show_food(request, food_id):
    food = Food.objects.get(id=food_id)
    return HttpResponse(f'<p style="text-align: center;font-size: large">Product: {food.name} details page</p>')
