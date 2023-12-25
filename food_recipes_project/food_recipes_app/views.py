from uuid import uuid4
from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm, RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient

MAX_RECIPES_AT_MAIN_PAGE = 6
MAIN_TITLE = _('Hello at simple recipes web application!')
CREATE_RECIPE_TITLE = _('Create recipe')
EDIT_RECIPE_TITLE = _('Edit recipe')
ACCESS_FORBIDDEN_MSG = _('Access forbidden!')
RECIPE_NOT_FOUND_MSG = _('Recipe not found...')

# Create your views here.
class Main(View):
    def get(self, request):
        recipes = Recipe.objects.order_by('?')
        
        context = {
            'title': MAIN_TITLE,
            'recipes': recipes[:MAX_RECIPES_AT_MAIN_PAGE],
        }
        return render(request, 'food_recipes_app/main.html', context=context)


class Register(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'food_recipes_app/registration.html', {'form': form, 'create': True})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main')
        return render(request, 'food_recipes_app/registration.html', {'form': form, 'create': True})


class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'food_recipes_app/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('main')
            else:
                bad_req = 'Bad username or password'
        return render(request, 'food_recipes_app/login.html', {'form': form, 'bad_req': bad_req})


class Logout(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('main')


class ReadRecipe(View):
    def get(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Recipe.DoesNotExist:
            return render(request, 'food_recipes_app/not_found_404.html', {'title': RECIPE_NOT_FOUND_MSG}, status=404)

        recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        duration_formatted = get_duration_formatted(recipe.cooking_duration)

        previous_recipe_id = recipe_id - 1 if recipe_id > 1 else 0
        next_recipe_id = recipe_id + 1
        
        context = {
            'title': CREATE_RECIPE_TITLE,
            'recipe': recipe,
            'ingredients': recipe_ingredients,
            'duration_formatted': duration_formatted,
            "previous_recipe_id": previous_recipe_id, 
            "next_recipe_id":next_recipe_id
        }
        return render(request, 'food_recipes_app/read_recipe.html', context=context)


class CreateRecipe(View):
    def get(self, request):
        form = RecipeForm()
        RecipeIngredientFormSet = inlineformset_factory(Recipe, RecipeIngredient, form=RecipeIngredientForm, extra=5)
        formset = RecipeIngredientFormSet(prefix='recipeingredient')
        context = {
            'title': CREATE_RECIPE_TITLE,
            'form': form,
            'formset': formset,
            'create': True
        }
        return render(request, 'food_recipes_app/create_recipe.html', context=context)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return render(request, 'food_recipes_app/not_found_404.html', {'title': ACCESS_FORBIDDEN_MSG}, status=403)

        form = RecipeForm(request.POST, request.FILES)        
        RecipeIngredientFormSet = inlineformset_factory(Recipe, RecipeIngredient, form=RecipeIngredientForm, extra=0)
        formset = RecipeIngredientFormSet(request.POST, prefix='recipeingredient')

        if form.is_valid():            
            recipe = Recipe(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                dish_img=save_img(form.cleaned_data['dish_img']),
                category=form.cleaned_data['category'],
                difficulty=form.cleaned_data['difficulty'],
                cooking_steps=form.cleaned_data['cooking_steps'],
                cooking_duration=form.cleaned_data['cooking_duration'],
                author_id=request.user.id
            )
            recipe.save()
            
            formset = RecipeIngredientFormSet(request.POST, prefix='recipeingredient', instance=recipe)
            if formset.is_valid():
                for form in formset:
                    if 'DELETE' in form.changed_data:
                        continue
                    try:
                        ingredient = form.cleaned_data['ingredient']
                        quantity = form.cleaned_data['quantity']
                        recipe_ingredient = RecipeIngredient(recipe=recipe, ingredient=ingredient, quantity=quantity)
                        recipe_ingredient.save()
                        print(ingredient.name, quantity)
                    except KeyError:
                        break
                return redirect('read_recipe', recipe_id=recipe.pk)
        
        context = {
            'title': CREATE_RECIPE_TITLE,
            'form': form,
            'formset': formset,
            'create': True
        }
        return render(request, 'food_recipes_app/create_recipe.html', context=context)

class UpdateRecipe(View):
    def get(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Recipe.DoesNotExist:
            return render(request, 'food_recipes_app/not_found_404.html', {'title': ACCESS_FORBIDDEN_MSG}, status=403)
        
        form = RecipeForm(instance=recipe)
        RecipeIngredientFormSet = inlineformset_factory(Recipe, RecipeIngredient, form=RecipeIngredientForm, extra=3)
        formset = RecipeIngredientFormSet(instance=recipe, prefix='recipeingredient')
        context = {
            'title': EDIT_RECIPE_TITLE,
            'form': form,
            'formset': formset,
            'create': False,
            'recipe_id': recipe.pk
        }
        return render(request, 'food_recipes_app/create_recipe.html', context=context)
    
    def post(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                img = form.cleaned_data['dish_img']
                recipe.dish_img = save_img(img)
            recipe.name = form.cleaned_data['name']
            recipe.description = form.cleaned_data['description']
            recipe.category = form.cleaned_data['category']
            recipe.difficulty = form.cleaned_data['difficulty']
            recipe.cooking_steps =form.cleaned_data['cooking_steps']
            recipe.cooking_duration = form.cleaned_data['cooking_duration']
            recipe.save()  

        RecipeIngredientFormSet = inlineformset_factory(Recipe, RecipeIngredient, form=RecipeIngredientForm, extra=0)
        formset = RecipeIngredientFormSet(request.POST, prefix='recipeingredient', instance=recipe)
        if formset.is_valid():
            recipe.ingredients.clear()
            for form in formset:
                if 'DELETE' in form.changed_data:
                    continue
                try:
                    ingredient = form.cleaned_data['ingredient']
                    quantity = form.cleaned_data['quantity']
                    recipe_ingredient = RecipeIngredient(recipe=recipe, ingredient=ingredient, quantity=quantity)
                    recipe_ingredient.save()
                except KeyError:
                    break
            return redirect('read_recipe', recipe_id=recipe.pk)
        
        context = {
            'title': EDIT_RECIPE_TITLE,
            'form': form,
            'formset': formset,
            'create': False,
            'recipe_id': recipe_id
        }
        return render(request, 'food_recipes_app/create_recipe.html', context=context)


def save_img(image):
        name = '.'.join((str(uuid4()), image.name.split('.')[-1]))
        fs = FileSystemStorage()
        fs.save(name, image)
        return name


def get_duration_formatted(duration):    
    duration_in_minutes = duration.total_seconds() // 60
    hours = int(duration_in_minutes) // 60
    minutes = int(duration_in_minutes) % 60
    return f"{hours} ч. {minutes} м." if hours else f"{minutes} м."
