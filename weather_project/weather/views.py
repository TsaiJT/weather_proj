import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

# Create your views here.
def weather_view(request):


    url_weather_api = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=bd45fc9db8849cb46d00a451483ccd44'

    err_msg = ''
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            exist = City.objects.filter(name = new_city).count()
            if exist == 0:
                response = requests.get(url_weather_api.format(new_city)).json()
                if response['cod'] == 200:
                    form.save()
                else:
                    err_msg = "Incorrect Location"
            else:
                err_msg = "Already Existing"
                
    print(err_msg)
    form = CityForm()

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        response = requests.get(url_weather_api.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : response['main']['temp'],
            'description' : response['weather'][0]['description']
        }
        weather_data.append(city_weather)

    print(weather_data)

    context = {'weather_data' : weather_data, 'form' : form, 'message' : err_msg}

    return render(request, 'weather/weather.html', context)