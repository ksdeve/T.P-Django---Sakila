from django.urls import path
from sakila.views import status, country_list, city_list, cities_by_country, search, film_detail, film_list, login_view

urlpatterns = [
    path('hello/', status, name='banniere'),
    path('countries/', country_list, name='country_list'),
    path('cities/', city_list, name='city_list'),
    path('films/', film_list, name='film_list'),

    path('countries/<int:country_id>/cities/', cities_by_country, name='cities_by_country'),

    path('films/<int:pk>/', film_detail, name='film_detail'),
    path('', login_view, name='login'),


    path('search/', search, name='search')

]
