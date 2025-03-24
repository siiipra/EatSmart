from django.contrib import admin
from .models import Food, Ingredient, FoodIngredients, NutritionalDetail


# Register your models here.
admin.site.register(Food)
admin.site.register(Ingredient)
admin.site.register(FoodIngredients)
admin.site.register(NutritionalDetail)