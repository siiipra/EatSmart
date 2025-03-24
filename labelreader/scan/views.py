from django.shortcuts import render
from .models import Food, FoodIngredients, NutritionalDetail
from django.http import HttpResponse


def index(request):
    return render(request, 'scan/index.html')

def search(request):
    if "search_food" in request.GET:
        search_term = request.GET["search_food"]
        results= Food.objects.filter(name__contains =search_term)
        print("length is" + str(len(results)))
        for result in results:
            print(result)
        return render(request, 'scan/search.html',{"results": results})
    return render(request, 'scan/search.html')

def details(request, food_id):
    food = Food.objects.get(id= food_id)
    return render(request, 'scan/details.html', {"food" : food})

def compare(request):
    print(request.GET)
    food1=None
    food2=None
    food3=None

    context = {}

    if "food1" in request.GET:
        food1 = Food.objects.get(id=request.GET["food1"])
        food1_nutrition = NutritionalDetail.objects.filter(food=food1)[0]
        food1_ingredients = FoodIngredients.objects.filter(food=food1)
        print(food1_nutrition)
        print(food1_ingredients)
        context["food1"] = food1
        context["food1_nutrition"] = food1_nutrition
        context["food1_ingredients"] = food1_ingredients
    if "food2" in request.GET:
        food2 = Food.objects.get(id=request.GET["food2"])
        context["food2"] = food2
    if "food3" in request.GET:
        food3 = Food.objects.get(id=request.GET["food3"])
        context["food3"] = food3
    return render(request, 'scan/compare.html', context)




# Create your views here.
