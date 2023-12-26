from django.urls import path
from . import views

urlpatterns = [
    path('', views.Main.as_view(), name='main'),    
    path('about/', views.About.as_view(), name='about'),
    path('faq/', views.Faq.as_view(), name='faq'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('registration/', views.Register.as_view(), name='register'),
    path('categories/', views.Categories.as_view(), name='categories'),
    path('category/<int:category_id>/', views.CategoryView.as_view(), name='read_category'),
    path('ingredients/', views.IngredientsView.as_view(), name='ingredients'),
    path('create/', views.CreateRecipe.as_view(), name='create_recipe'),
    path('edit/<int:recipe_id>/', views.UpdateRecipe.as_view(), name='edit_recipe'),
    path('recipe/<int:recipe_id>/', views.ReadRecipe.as_view(), name='read_recipe'),
    path('search/', views.Search.as_view(), name='search'),
]
