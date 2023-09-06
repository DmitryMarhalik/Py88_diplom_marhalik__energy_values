from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Food(models.Model):
    name = models.CharField(max_length=30, unique=True, db_index=True)
    bar_code = models.CharField(max_length=14, unique=True, db_index=True, null=True, blank=True)
    image = models.ImageField(upload_to='image_food/%Y/%m/%d', null=True, blank=True)
    proteins = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    fats = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    kcal = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True)
    be_confirmed = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ('name', 'category')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_food', kwargs={'food_id': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name="URL category")

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('category', kwargs={'cat_id': self.pk})

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('id','name',)


class Intake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey('Food', on_delete=models.CASCADE)
    gram = models.DecimalField(max_digits=5, decimal_places=1)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
