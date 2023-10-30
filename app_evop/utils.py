from app_evop.models import Category

tabs = [{'title': 'Add Food 🍟', 'url_name': 'add_food'},
        {'title': 'Intake 📅', 'url_name': 'intake'},
        {'title': 'My Intakes 📝', 'url_name': 'calculation_intakes'},
        {'title': 'My Norm Kcal 🏓', 'url_name': 'calculation_norma_kcal'},
        {'title': 'Feedback 📧', 'url_name': 'feedback'},
        ]

no_auth_tabs = [{'title': 'Feedback 📧', 'url_name': 'feedback'}]
categories = Category.objects.all()


class ContextMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['categories'] = categories
        if not self.request.user.is_authenticated:
            context['tabs'] = no_auth_tabs
        else:
            context['tabs'] = tabs
        if 'cat_selected' not in context:
            context['cat_selected'] = None
        return context
