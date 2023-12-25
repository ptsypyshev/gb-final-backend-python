from django.contrib import admin
from .models import Category, Ingredient, Recipe, RecipeIngredient, Unit


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ('id', 'name', 'category', 'difficulty', 'cooking_duration',
                    'author', 'updated_at')
    list_filter = ('category', 'difficulty', 'cooking_duration', 'author', 'updated_at')
    ordering = ('id',)
    search_fields = ('name', 'description', 'cooking_steps')


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('measure_unit', )
    ordering = ('name',)
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)


class UnitAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)


# Register your models here.
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Unit, UnitAdmin)
