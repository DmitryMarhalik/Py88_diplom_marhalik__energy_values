from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bar_code', 'preview_pict', 'proteins',
                    'fats', 'carbohydrates', 'kcal', 'category', 'be_confirmed')
    list_display_links = ('name',)
    search_fields = ('name', 'bar_code')
    list_editable = ('be_confirmed',)
    list_filter = ('category', 'be_confirmed')
    readonly_fields = ('preview_pict',)

    def preview_pict(self, instance: Food):
        if not instance.image:
            return mark_safe(f'<b>without logo</b>')
        else:
            return mark_safe(f'<img src="/media/{instance.image}" style ="max-width:40px">')


# 'image_food/%Y/%m/%d'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class IntakeAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'food_id', 'gram', 'time')
    list_display_links = ('user_id',)
    search_fields = ('user_id',)
    list_filter = ('time',)


admin.site.register(Food, FoodAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Intake, IntakeAdmin)
