from django.shortcuts import render
from datetime import datetime
from sakila.models import Country
from sakila.models import City
from sakila.models import Film
from sakila.models import Actor
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Create your views here.
def status(request):
    h = datetime.now().strftime("%Y-%m- %d - %H:%M:%S")
    cname = "Kévin S"
    return render(request, 'banniere.html', {'hours': h, 'cname': cname})


def country_list(request):
    countries = Country.objects.all()
    return render(request, 'country_list.html', {'countries': countries})



def city_list(request):
    cities = City.objects.select_related('country').all()
    return render(request, 'city_list.html', {'cities': cities})

# views.py
def cities_by_country(request, country_id):
    cities = City.objects.filter(country_id=country_id)
    country = Country.objects.get(pk=country_id)
    return render(request, 'cities_by_country.html', {'cities': cities, 'country': country})


def film_list(request):
    films = Film.objects.all()
    return render(request, 'film_list.html', {'films': films})



def film_detail(request, pk):
    film = get_object_or_404(Film, pk=pk)
    return render(request, 'film_detail.html', {'film': film})


def search(request):
    query = request.GET.get('q', '').strip()
    films = Film.objects.filter(title__icontains=query) if query else Film.objects.none()
    actors = Actor.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query)
    ) if query else Actor.objects.none()
    return render(request, 'search.html', {
        'query': query,
        'films': films,
        'actors': actors,
    })