from django.shortcuts import render
from datetime import datetime
from sakila.models import Country
from sakila.models import City
from sakila.models import Film
from sakila.models import Actor
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from sakila.forms import LoginForm
from sakila.models import User
import bcrypt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from sakila.decorator import my_login_required


@my_login_required
def status(request):
    h = datetime.now().strftime("%Y-%m- %d - %H:%M:%S")
    cname = "Kévin S"
    return render(request, 'banniere.html', {'hours': h, 'cname': cname})

@my_login_required
def country_list(request):
    countries = Country.objects.all()
    return render(request, 'country_list.html', {'countries': countries})


@my_login_required
def city_list(request):
    cities = City.objects.select_related('country').all()
    return render(request, 'city_list.html', {'cities': cities})

@my_login_required
def cities_by_country(request, country_id):
    cities = City.objects.filter(country_id=country_id)
    country = Country.objects.get(pk=country_id)
    return render(request, 'cities_by_country.html', {'cities': cities, 'country': country})

@my_login_required
def film_list(request):
    films = Film.objects.all()
    return render(request, 'film_list.html', {'films': films})

@my_login_required
def search(request):
    query = request.GET.get('q', '')
    films = Film.objects.filter(title__icontains=query)
    actors = Actor.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query)
    )
    return render(request, 'search.html', {'films': films, 'actors': actors, 'query': query})
@my_login_required
def film_detail(request, pk):
    film = get_object_or_404(Film, pk=pk)
    return render(request, 'film_detail.html', {'film': film})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            try:
                user = User.objects.get(username=uname)
                if bcrypt.checkpw(pwd.encode(), user.password.encode()):
                    request.session['user_id'] = user.id
                    return redirect('banniere')  # ou une autre page
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except User.DoesNotExist:
                messages.error(request, "Utilisateur non trouvé.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


