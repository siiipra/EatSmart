from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search" ),
    path("details/<int:food_id>", views.details, name="details" ),
    path("compare/", views.compare, name="compare"),

]