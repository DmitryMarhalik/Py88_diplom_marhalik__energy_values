from django import template

from app_evop.models import Category

register = template.Library()

@register.inclusion_tag('evop/list_categories.html')
def show_categories(cat_selected=0):

    cats = Category.objects.all()
    return {"categories": cats, "cat_selected": cat_selected}
