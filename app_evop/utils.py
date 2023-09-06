from .models import Category

tabs = [{'title': 'Add Food 🍟', 'url_name': 'add_food'},
        {'title': 'Intake 📅', 'url_name': 'intake'},
        {'title': 'Calculation Result 📝', 'url_name': 'calculation_result'},
        {'title': 'Feedback 📧', 'url_name': 'feedback'},
        ]


class ContextMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.all()
        menu = tabs.copy()
        if not self.request.user.is_authenticated:
            del menu[:3]
            # tabs.pop(0)

        context['tabs'] = menu
        # context['cats'] = categories
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
