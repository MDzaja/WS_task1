"""electric_vehicles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from app import views


urlpatterns = [
    path('recipes/', views.recipes, name='recipes'),
    path('recipe/<recipe_id>', views.recipe_details, name='recipe_details'),
    path('add-ingredient/', views.add_ingredient, name='add_ingredient'),
    path('update-ingredient/', views.update_ingredient, name='update_ingredient'),
    path('delete-ingredient/', views.delete_ingredient, name='delete_ingredient'),
    path('', views.home, name='home'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('categories/', views.categories, name='categories'),
    path('techniques/', views.techniques, name='techniques'),
    path('beverages/', views.dbpedia_beverages, name='beverages'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('insert-new-recipe', views.insert_new_recipe, name='insert_new_recipe')

]
