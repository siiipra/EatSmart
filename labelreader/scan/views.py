from django.shortcuts import render
from .models import Food, FoodIngredients, NutritionalDetail, Ingredient
from django.http import HttpResponse
from django.http import JsonResponse
import requests


def index(request):
    return render(request, 'scan/home.html')


def search(request):
    if "search_food" in request.GET:
        search_term = request.GET["search_food"]
        results = Food.objects.filter(name__contains=search_term)
        nutritionaldetails = NutritionalDetail.objects.filter(food__in=results)
        print("length is" + str(len(results)))
        for result in results:
            print(result)
        return render(request, 'scan/search.html', {"results": results, "nutritionaldetails": nutritionaldetails})
    return render(request, 'scan/search.html')


def search_api(request):
    if "search_food" in request.GET:
        search_term = request.GET["search_food"]
        results = Food.objects.filter(name__contains=search_term)
        print("length is" + str(len(results)))
        for result in results:
            print(result)
        data = {"results": [
            {
                "name": result.name,
                "id": result.id
            }
            for result in results
        ]}
        return JsonResponse(data)


def details(request, food_id):
    food = Food.objects.get(id=food_id)
    nutrition = NutritionalDetail.objects.filter(food=food)[0]
    food_ingredients = FoodIngredients.objects.filter(food=food)
    return render(request, 'scan/details.html', {"food": food, "nutrition": nutrition, "food_ingredients": food_ingredients})


def compare(request):
    print(request.GET)
    food1 = None
    food2 = None
    food3 = None

    context = {}

    if "food1" in request.GET:
        query1 = request.GET["food1"]
        food1 = Food.objects.get(id=query1)
        food1_nutrition = NutritionalDetail.objects.filter(food=food1)[0]
        food1_ingredients = FoodIngredients.objects.filter(food=food1)
        context["food1"] = food1
        context["food1_nutrition"] = food1_nutrition
        context["food1_ingredients"] = food1_ingredients
    if "food2" in request.GET:
        query2 = request.GET["food2"]
        food2 = Food.objects.get(id=query2)
        food2_nutrition = NutritionalDetail.objects.filter(food=food2)[0]
        food2_ingredients = FoodIngredients.objects.filter(food=food2)
        context["food2"] = food2
        context["food2_nutrition"] = food2_nutrition
        context["food2_ingredients"] = food2_ingredients
    if "food3" in request.GET:
        food3 = Food.objects.get(id=request.GET["food3"])
        food3_nutrition = NutritionalDetail.objects.filter(food=food3)[0]
        food3_ingredients = FoodIngredients.objects.filter(food=food3)
        context["food3"] = food3
        context["food3_nutrition"] = food3_nutrition
        context["food3_ingredients"] = food3_ingredients
    return render(request, 'scan/compare.html', context)


def add_food(request):
    if request.method == 'POST':
        print(request.POST)
        food_name = request.POST['food_name']
        food_calories = request.POST['food_calories']
        food_brand = request.POST['food_brand']
        food_category = request.POST['food_category']
        food_barcode = request.POST['food_barcode']
        food_fssainumber = request.POST['food_fssainumber']
        food_image = request.FILES.get('food_image')
        food_carbs = request.POST['food_carbs']
        food_totalsugar = request.POST['food_totalsugar']
        food_addedsugar = request.POST['food_addedsugar']
        food_protein = request.POST['food_protein']
        food_fat = request.POST['food_fat']
        food_saturatedfat = request.POST['food_saturatedfat']
        food_transfat = request.POST['food_transfat']
        food_fibre = request.POST['food_fibre']
        food_sodium = request.POST['food_sodium']
        food_cholesterol = request.POST['food_cholesterol']
        ingredient_1 = request.POST['ingredient_1']
        ingredient_2 = request.POST['ingredient_2']
        ingredient_3 = request.POST['ingredient_3']
        ingredient_4 = request.POST['ingredient_4']
        ingredient_5 = request.POST['ingredient_5']
        ingredient_6 = request.POST['ingredient_6']
        ingredient_7 = request.POST['ingredient_7']
        ingredient_8 = request.POST['ingredient_8']
        ingredient_9 = request.POST['ingredient_9']
        ingredient_10 = request.POST['ingredient_10']

        food = Food(name=food_name, brand=food_brand, category=food_category, barcode=food_barcode, fssai_number=food_fssainumber, image=food_image)
        food.save()
        nutrition = NutritionalDetail(food=food, quantity=100, quantity_unit="gram", energy=food_calories,
                                      carbohydrate=food_carbs, total_sugar=food_totalsugar,
                                      added_sugar=food_addedsugar, total_fat=food_fat, saturated_fat=food_saturatedfat,
                                      trans_fat=food_transfat, protein=food_protein, fibre=food_fibre, sodium=food_sodium,
                                      cholesterol=food_cholesterol)
        nutrition.save()
        ingredients = [ingredient_1, ingredient_2, ingredient_3, ingredient_4, ingredient_5, ingredient_6, ingredient_7, ingredient_8, ingredient_9, ingredient_10]
        ingredient_rank = 1
        while ingredient_rank <= 10:
            if ingredients[ingredient_rank-1] == "":
                pass
            else:
                ingredient = Ingredient.objects.get(id=ingredients[ingredient_rank-1])
                foodingredient = FoodIngredients(food=food, ingredient=ingredient, ingredient_rank=ingredient_rank)
                foodingredient.save()
            ingredient_rank = ingredient_rank + 1
        return render(request, 'scan/add_food.html')
    else:
        food_details = {"food_name": "Good day"}
        if "barcode" in request.GET:
            barcode = request.GET['barcode']
            food_details = get_open_food_facts_details(barcode)
            print(barcode)
        ingredients = Ingredient.objects.all()
        return render(request, 'scan/add_food.html', {"ingredients": ingredients,
                                                      "ingredient_rank": range(1, 11), "food_details": food_details})

def get_open_food_facts_details(barcode):
    url = f"https://world.openfoodfacts.org/api/v3/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch data")
        return {"error": "Failed to fetch data"}

    data = response.json()

    try:
        product = data['product']
        nutriments = product.get('nutriments', {})

        food_data = {
            'food_name': product.get('product_name', 'N/A'),
            'food_calories': nutriments.get('energy-kcal_100g', 'N/A'),
            'food_carbs': nutriments.get('carbohydrates_100g', 'N/A'),
            'food_totalsugar': nutriments.get('sugars_100g', 'N/A'),
            'food_fat': nutriments.get('fat_100g', 'N/A'),
            'food_protein': nutriments.get('proteins_100g', 'N/A'),
            'food_fiber': nutriments.get('fiber_100g', 'N/A'),
            'food_sodium': nutriments.get('sodium_100g', 'N/A'),
            'ingredients_text': product.get('ingredients_text', 'N/A'),
            'food_brand': product.get('brands', 'N/A'),
            'food_category': product.get('categories', 'N/A'),
            'food_fssai_number': product.get('packaging_code', 'N/A'),
            'food_addedsugar': nutriments.get('added-sugars_100g', 'N/A'),
            'food_saturatedfat': nutriments.get('saturated-fat_100g', 'N/A'),
            'food_transfat': nutriments.get('trans-fat_100g', 'N/A'),
            'food_cholesterol': nutriments.get('cholesterol_100g', 'N/A'),
            'food_ingredient_list': nutriments.get['ingredients_text']
        }

        print(food_data)
        return food_data

    except KeyError:
        print("Unexpected response structure")
        return {"error": "Unexpected response structure"}


# Create your views here.
