from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("search/", views.search, name="search" ),
    path("details/<int:food_id>", views.details, name="details" ),
    path("compare/", views.compare, name="compare"),
    path('api/search/', views.search_api, name='search_api'),
    path("add_food/", views.add_food, name='add_food'),

]