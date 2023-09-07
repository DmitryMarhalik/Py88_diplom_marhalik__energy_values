tabs = [{'title': 'Add Food 🍟', 'url_name': 'add_food'},
        {'title': 'Intake 📅', 'url_name': 'intake'},
        {'title': 'Calculation Result 📝', 'url_name': 'calculation_result'},
        {'title': 'Feedback 📧', 'url_name': 'feedback'},
        ]

no_authtabs = [{'title': 'Feedback 📧', 'url_name': 'feedback'}]


class ContextMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        if not self.request.user.is_authenticated:
            context['tabs'] = no_authtabs
        else:
            context['tabs'] = tabs
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
