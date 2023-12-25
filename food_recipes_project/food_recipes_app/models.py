import uuid
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

DIFFICULTY_EASY = 1
DIFFICULTY_MEDIUM = 2
DIFFICULTY_HARD = 3
DIFFICULTIES = (
    (DIFFICULTY_EASY, _('Difficulty|easy')),
    (DIFFICULTY_MEDIUM, _('Difficulty|medium')),
    (DIFFICULTY_HARD, _('Difficulty|hard')),
)

# Create your models here.
class Unit(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name=_('Unit|name'))
    name_abbrev = models.CharField(max_length=60, blank=True, verbose_name=_('Unit|name_abbrev'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')
        ordering = ["name"]

class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Ingredient|name'))
    measure_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name = _('Unit'))

    def __str__(self):
        return f'{self.name} ({self.measure_unit})'
    
    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')
        ordering = ["name"]


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Category|name'))
    description = models.TextField(blank=True, verbose_name=_('Category|description'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    

def gen_name(instance, filename):
    name = '.'.join((str(uuid.uuid4()), filename.split('.')[-1]))
    return name


class Recipe(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Recipe|name'))
    description = models.TextField(verbose_name=_('Recipe|description'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name = _('Category'))
    difficulty = models.SmallIntegerField(choices=DIFFICULTIES, default=DIFFICULTY_MEDIUM, verbose_name=_('Recipe|difficulty'))
    cooking_steps = models.TextField(verbose_name=_('Recipe|cooking_steps'))
    cooking_duration = models.DurationField(verbose_name=_('Recipe|cooking_duration'))
    dish_img = models.ImageField(upload_to=gen_name, blank=True, verbose_name=_('Recipe|dish_img'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Recipe|author'))
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', verbose_name = _('Ingredients'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
        ordering = ["name"]
    
    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name = _('Ingredient'))
    quantity = models.DecimalField(decimal_places=2, max_digits=12, verbose_name = _('Quantity'))

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')

    def __str__(self):
        return self.ingredient.name
