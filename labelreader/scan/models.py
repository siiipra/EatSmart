from django.db import models


# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    barcode = models.CharField(max_length=50)
    fssai_number = models.CharField(max_length=50)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50)


class FoodIngredients(models.Model):
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    ingredient_rank = models.IntegerField()


class NutritionalDetail(models.Model):
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    quantity_unit = models.CharField(max_length=50)
    energy = models.FloatField()
    carbohydrate = models.FloatField()
    total_sugar = models.FloatField(default=None)
    added_sugar = models.FloatField(default=None)
    total_fat = models.FloatField()
    saturated_fat = models.FloatField(default=None)
    trans_fat = models.FloatField(default=None)
    protein = models.FloatField()
    fibre = models.FloatField(default=None)
    sodium = models.FloatField(default=None)
    cholesterol = models.FloatField(default=None)

