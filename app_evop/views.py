from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, FormView
from django.conf import settings

from app_evop.forms import IntakeForm, AddFoodForm, CalculationResultForm, RegisterUserForm, FeedbackForm
from app_evop.models import Food
from app_evop.utils import ContextMixin, tabs, categories
from app_evop.calculation_user_intakes import intakes_between_days


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
    paginate_by = 13
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
        try:
            send_mail('EVOP site',
                      message,
                      self.request.user.email,
                      [settings.EMAIL_HOST_USER]
                      )
        except BadHeaderError:  # BadHeaderError, чтобы предотвратить вставку злоумышленниками
            #  дополнительных заголовков электронной почты. Если обнаружен “плохой заголовок”,
            #  то представление вернет клиенту HttpResponse с текстом “Incorrect header found”.
            return HttpResponse('Incorrect header found')
        return redirect('success', args=f'food {food}')


class ShowCategory(ContextMixin, ListView):
    paginate_by = 10
    template_name = 'evop/show_category.html'
    context_object_name = 'foods'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Category : ' + str(context['foods'][0].category.name),
                                             cat_selected=context['foods'][0].category.slug)
        context.update(user_context)
        return context

    def get_queryset(self):
        cat_slug = self.kwargs['cat_slug']  # c.get_absolute_url(basis)--(!!get_abs_url.models.kwargs!!)
        return Food.objects.filter(category__slug=cat_slug, be_confirmed=True).order_by('-id')


class AddIntake(ContextMixin, CreateView):
    form_class = IntakeForm
    template_name = 'evop/intake.html'

    # success_url = reverse_lazy('success_add_intake')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Intake')
        context.update(user_context)
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        form.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        context = super().get_context_data(**kwargs)
        intake = context.get('intake').food.name
        return reverse('success', args=[f'intake {intake}'])


class CalculetionResult(ContextMixin, FormView):
    template_name = 'evop/calculation_result.html'
    form_class = CalculationResultForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Calculation')
        context.update(user_context)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_user_context()
        days = request.POST.get('days')
        energy_values, count_of_products, message = intakes_between_days(request, days)
        context = {'tabs': context['tabs'], 'categories': context['categories'],
                   'title': 'Final calculation',
                   'energy_values': energy_values,
                   'count_product': count_of_products, 'message': message
                   }
        if not count_of_products:
            context['title'] = 'No result'
        return render(request, 'evop/final_result.html',
                      context=context)


class FeedBack(ContextMixin, FormView):  # Formview не привязано к модели
    form_class = FeedbackForm
    template_name = 'evop/feedback.html'

    # success_url = reverse_lazy('success_send_message')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Feedback')
        context.update(user_context)
        return context

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        name = form.cleaned_data.get('name')
        content = form.cleaned_data.get('content')
        message = f'name: {name}\nemail: {email}\nmessage: {content}'
        try:
            send_mail('EVOP site',
                      message,
                      email,
                      [settings.EMAIL_HOST_USER]
                      )
        except BadHeaderError:  # BadHeaderError, чтобы предотвратить вставку злоумышленниками
            #  дополнительных заголовков электронной почты. Если обнаружен “плохой заголовок”,
            #  то представление вернет клиенту HttpResponse с текстом “Incorrect header found”.
            return HttpResponse('Incorrect header found')
        return redirect('success', args=f'feedbackname {name}')


class SignIn(ContextMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'evop/sign_in.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Sign In')
        context.update(user_context)
        return context

    def get_success_url(self, **kwargs):
        username = self.request.user.username
        return reverse('success', args=[f'username {username}'])
        # return redirect('home')


class SignUp(ContextMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'evop/sign_up.html'

    # success_url = reverse_lazy('success_registration_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Sign Up')
        context.update(user_context)
        return context

    def get_success_url(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = context.get('user').username
        return reverse('success', args=[f'reg_user {username}'])

    # def form_valid(self, form):        #для автоматического входа при регистрации
    #     user=form.save()
    #     login(self.request, user)
    #     return redirect('home')


def sign_out_user(request):
    logout(request)
    return redirect('home')


def success(request, args):  # 'food 23r3t5 2435t 35t we'
    keyword = args.split(' ')[:1][0]
    arg = args.split(' ')[1:]
    arg = ' '.join(arg)
    try:
        return render(request, 'evop/success.html', {'tabs': tabs,
                                                     keyword: arg, 'categories': categories})
    except:
        return HttpResponse('<h1>Somethink went wrong. Go back and try again</h1>')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>404 --> Page Not Found 😔</h1>')


def show_food(request, food_id):
    food = Food.objects.get(id=food_id)
    return HttpResponse(f'<p style="text-align: center;font-size: large">Product: {food.name} details page</p>')
