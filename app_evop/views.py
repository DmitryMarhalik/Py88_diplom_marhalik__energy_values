from collections import Counter
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core import paginator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseNotFound, HttpResponse, Http404, request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from .models import Food
from .forms import *
from .utils import *


class HomePage(ContextMixin, ListView):
    model = Food
    template_name = 'evop/main.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Main page')  # to DataMixin
        # context = dict(list(context.items()) + list(user_context.items())) #or
        context.update(user_context)
        return context


# def main_page(request):
#     context = {
#         'tabs': tabs,
#         'title': 'Main Page',
#     }
#     return render(request, 'evop/main.html', context=context)


class AllFoods(ContextMixin, ListView):
    paginate_by = 10
    model = Food
    template_name = 'evop/all_foods.html'
    context_object_name = 'foods'

    # extra_context = {'title': 'AllFoods'}  передача статических, неизменяемых данных
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['tabs'] = tabs
    #     context['title'] = 'All Foods'
    #     context['cat_selected'] = 0
    #     return context #

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='All foods', cat_selected='all_foods')  # ????to or in  DataMixin
        context.update(user_context)
        return context

    def get_queryset(self):
        return Food.objects.all().filter(be_confirmed=True)


# def all_foods(request):
#     foods = Food.objects.all().order_by('id')
#     if not len(foods):
#         return HttpResponse('<h1>Database is empty :(</h1>')
#     else:
#         context = {
#             'tabs': tabs,
#             'food': foods,
#             'title': 'All Foods',
#         }
#     return render(request, 'evop/all_foods.html', context=context)


class AddIntake(LoginRequiredMixin, ContextMixin, CreateView):
    form_class = IntakeForm
    template_name = 'evop/intake.html'
    # success_url = reverse_lazy('success_add_intake')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Intake')  # to DataMixin
        context.update(user_context)
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        form.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        context = super().get_context_data(**kwargs)
        intake = context.get('intake').food.name
        # username = self.request.user.username
        return reverse('success', args=[{'intake': intake}])


class AddFood(ContextMixin, CreateView):  # LoginRequiredMixin,
    form_class = AddFoodForm
    template_name = 'evop/add_food.html'
    # success_url = reverse_lazy('success_add_food')
    # login_url = '/admin/' #to admin page
    # raise_exception = True  # 403 forbidden
    # login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Add food')  # to DataMixin
        context.update(user_context)
        return context

    def get_success_url(self, **kwargs):
        context = super().get_context_data(**kwargs)
        food = context.get('food').name
        return reverse('success', args=[{'food': food}])


class SignIn(ContextMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'evop/sign_in.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Sign In')  # to DataMixin
        context.update(user_context)
        return context

    def get_success_url(self, **kwargs):
        username = self.request.user.username
        return reverse('success', args=[{'name': username}])
        # return redirect('home')


def success(request, args):  # {'name': 'Dima'}
    arg = args.split(' ').pop()[1:-2]  # 'Dima'}-->Dima
    if 'name' in args:
        return render(request, 'evop/success.html', {'tabs': tabs, 'username': arg})
    elif 'food' in args:
        return render(request, 'evop/success.html', {'tabs': tabs, 'food': arg})
    elif 'feedback' in args:
        return render(request, 'evop/success.html', {'tabs': tabs, 'feedbackname': arg})
    elif 'reg_user' in args:
        return render(request, 'evop/success.html', {'tabs': tabs, 'reg_user': arg})
    elif 'intake' in args:
        return render(request, 'evop/success.html', {'tabs': tabs, 'intake': arg})
    else:
        HttpResponse('<h1>Somethink went wrong</h1>')


# def success_add_food(request, food):
#     return render(request, 'evop/success_add_food.html',
#                   {'tabs': tabs, 'food': food})


# def success_add_food(request, food):
#     return render(request, 'evop/success_add_food.html',
#                   {'tabs': tabs, 'food': food})
#
#
# def success_add_intake(request):
#     return render(request, 'evop/success_add_intake.html',
#                   {'tabs': tabs})

#
# def success_sign_in(request, name):
#     return render(request, 'evop/success_sign_in.html',
#                   {'tabs': tabs, 'name': name})

# def get_success_url(self, **kwargs):
#     # context = super().get_context_data(**kwargs)
#     # print(context)
#     # # print(type(context.values())[0].name)
#     # # print(type(context.get('object').name))
#     # fname = context.get('food').name
#     return reverse('home')
#
# def get_queryset(self):
#     return Food.objects.all().filter(be_confirmed=True).order_by('name')


# def intake(request):
#     if request.method == 'POST':
#         form = IntakeForm(request.POST)
#         if form.is_valid():
#             form.cleaned_data.update({'user_id': request.user.id})
#             try:
#                 Intake.objects.create(**form.cleaned_data)
#                 return HttpResponse('<h1>Success add intake</h1><a href="/"><--back</a>')
#             except:
#                 form.add_error(None, 'Error creating')
#
#     else:
#         form = IntakeForm()
#     return render(request, 'evop/intake.html',
#                   {'form': form, 'tabs': tabs, 'title': 'Добавление intake'})


# def success_feedback(request, name):
#     return render(request, 'evop/success_send_message.html',
#                   {'tabs': tabs, 'name': name})

#
# def success_registration_user(request, name):
#     return render(request, 'evop/success_registration_user.html',
#                   {'tabs': tabs, 'name': name})


# def add_food(request):
#     if request.method == 'POST':
#         form = AddFoodForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddFoodForm()
#     return render(request, 'evop/add_food.html',
#                   {'form': form, 'tabs': tabs, 'title': 'Add Food'})


class ShowCategory(ContextMixin, ListView):
    paginate_by = 3
    model = Food
    template_name = 'evop/show_category.html'
    context_object_name = 'foods'
    allow_empty = False

    def get_queryset(self):
        cat_slug = self.kwargs['cat_slug']
        return Food.objects.filter(category__slug=cat_slug, be_confirmed=True).order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Category : ' + str(context['foods'][0].category.name),
                                             cat_selected=context['foods'][0].category.slug)  # to DataMixin
        context.update(user_context)
        return context

        # context['tabs'] = tabs
        # context['title'] = 'Category : ' + str(context['foods'][0].category.name)
        # context['cat_selected'] = context['foods'][0].category.slug
        # return context


# def show_category(request, cat_id):
#     """with cat_id root url"""
#     food = Food.objects.filter(category_id=cat_id)
#     if len(food) == 0:
#         return HttpResponse('<h1>This category is empty</h1><a href="/"><--back</a>')
#     context = {
#         'foods': food,
#         'tabs': tabs,
#         'title': 'Display by category',
#         'cat_selected': cat_id,
#     }
#     return render(request, 'evop/show_category.html', context=context)


# def show_category(request, cat_slug):
#     cat = Category.objects.get(slug=cat_slug)
#     food = Food.objects.filter(category_id=cat.id)
#     if len(food) == 0:
#         return HttpResponse('<h1>This category is empty</h1><a href="/"><--back</a>')
#     context = {
#         'foods': food,
#         'tabs': tabs,
#         'title': 'Display by category',
#         'cat_selected': cat.id,
#     }
#     return render(request, 'evop/show_category.html', context=context)


class CalculetionResult(ContextMixin, ListView):
    paginate_by = 10
    # form_class = CalculationResultForm
    # template_name = 'evop/calculation_result.html'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user_context = self.get_user_context(title='Calculation')  # to DataMixin
    #     context.update(user_context)
    #     return context

    # def form_valid(self, form):
    #     days = form.cleaned_data.get('days')
    #     print(days)

    def get(self, request, *args, **kwargs):
        form = CalculationResultForm
        context = self.get_user_context(title='Calculation')
        return render(request, 'evop/calculation_result.html',
                      context={'form': form, 'title': context['title'], 'tabs': context['tabs']})

    def post(self, request, *args, **kwargs):
        context = self.get_user_context(title='Calculation')
        days = request.POST.get('days')
        days_ago = timezone.now() - timedelta(days=int(days))
        all_intake_product = (Intake.objects.values('food__name', 'food__proteins', 'food__fats',
                                                    'food__carbohydrates', 'food__kcal', 'gram').
                              filter(user_id=self.request.user.id, time__gte=days_ago))  # Queryset
        message = None
        if not all_intake_product:
            message = 'You have not consumed anything for a given period of time.'
            return render(request, 'evop/final_result.html',
                          context={'tabs': context['tabs'], 'title': 'No result', 'message': message})
        else:
            count_of_product = dict(
                Counter(all_intake_product.values_list('food__name')))  # {('chips',): 1,('water',):1}
            counts_of_products = dict(
                sorted({k[0]: v for k, v in count_of_product.items()}.items()))  # {'chips': 1, 'water': 1}
            proteins, fats, carbohydrates, kcal, gram = 0, 0, 0, 0, 0
            for energy_value in all_intake_product:
                proteins += float(energy_value['food__proteins']) * (float(energy_value['gram'] / 100))
                fats += float(energy_value['food__fats']) * (float(energy_value['gram'] / 100))
                carbohydrates += float(energy_value['food__carbohydrates']) * (float(energy_value['gram'] / 100))
                kcal += float(energy_value['food__kcal']) * (float(energy_value['gram'] / 100))
            dict_energy_values = {'proteins': round(proteins, 1), 'fats': round(fats, 1),
                                  'carbohydrates': round(carbohydrates, 1), 'kcal': round(kcal, 1)}
            return render(request, 'evop/final_result.html',
                          context={'tabs': context['tabs'], 'title': 'Final calculation',
                                   'energy_values': dict_energy_values,
                                   'count_product': counts_of_products, 'message': message
                                   })


def sign_out_user(request):
    logout(request)
    return redirect('home')


class SignUp(ContextMixin, CreateView):
    form_class = RegisterUserForm  # UserCreationForm  #
    template_name = 'evop/sign_up.html'
    # success_url = reverse_lazy('success_registration_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Sign Up')  # to DataMixin
        context.update(user_context)
        return context

    def get_success_url(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = context.get('user').username
        return reverse('success', args=[{'reg_user': username}])

    # def form_valid(self, form):                   #для автоматического входа при регистрации
    #     user=form.save()
    #     login(self.request, user)
    #     return redirect('home')
    #     username=self.request.user.username
    #     return reverse('success_registration_user',kwargs={'name': username})


# @login_required
# def feedback(request):
#     return HttpResponse('<h1>send email</h1>')

class FeedBack(ContextMixin, FormView):  # formview не привязано к модели
    form_class = FeedbackForm
    template_name = 'evop/feedback.html'
    # success_url = reverse_lazy('success_send_message')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Feedback')  # to DataMixin
        context.update(user_context)
        return context

    # def get_success_url(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     username = self.request.user.username
    #     return reverse('success_send_message', kwargs={'name': username})
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        name = form.cleaned_data.get("name")
        content = form.cleaned_data.get("content")
        message = f'name: {name}\nemail: {email}\nmessage: {content}'
        try:
            send_mail('EVOP site',
                      message,
                      email,
                      [settings.EMAIL_HOST_USER]
                      )
        except BadHeaderError:  # BadHeaderError, чтобы предотвратить вставку злоумышленниками
            # дополнительных заголовков
            # электронной почты. Если обнаружен “плохой заголовок”,
            # то представление вернет клиенту HttpResponse с текстом “Incorrect header found”.
            return HttpResponse('Incorrect header found')
        return redirect('success', args={'feedback': name})


# def success_send_message(request, name):
#     return render(request, 'evop/success_send_message.html',
#                   {'tabs': tabs, 'name': name})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>404 --> Page Not Found :(</h1>')


def show_food(request, food_id):
    food = Food.objects.get(id=food_id)
    return HttpResponse(f'food -- >{food.name}')
