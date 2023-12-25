from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Main, Register, Login, Logout, CreateRecipe, UpdateRecipe, ReadRecipe

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('registration/', Register.as_view(), name='register'),
    path('create/', CreateRecipe.as_view(), name='create_recipe'),
    path('edit/<int:recipe_id>/', UpdateRecipe.as_view(), name='edit_recipe'),
    path('recipe/<int:recipe_id>/', ReadRecipe.as_view(), name='read_recipe'),
]
