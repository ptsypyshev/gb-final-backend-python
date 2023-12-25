from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'category', 'difficulty', 'cooking_steps', 'cooking_duration', 'dish_img']
        widgets  = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название продукта'}),
            'description':  forms.Textarea(attrs={'class': 'form-control'}),
            'category':  forms.Select(attrs={'class': 'form-control'}),
            'difficulty':  forms.Select(attrs={'class': 'form-control'}),
            'cooking_steps':  forms.Textarea(attrs={'class': 'form-control'}),
            'cooking_duration':  forms.TimeInput(attrs={'class': 'form-control'}),
            'dish_img': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity']
        widgets  = {
            'ingredient':  forms.Select(attrs={'class': 'form-control'}),
            'quantity':  forms.NumberInput(attrs={'class': 'form-control'}),
        }


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets  = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        if commit:
            user.save()
            group_name = 'users'
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
