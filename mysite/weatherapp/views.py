import urllib.request
import json
import os
from django.shortcuts import render
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access API key from environment
api_key = os.getenv('OPENWEATHER_API_KEY')

def index(request):
    city = request.POST.get('city')  # Get the city name from the form

    if city:
        # URL encode the city name to handle spaces and special characters
        city_encoded = urllib.parse.quote(city)

        # Construct the API URL with the encoded city name
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_encoded}&appid={api_key}'

        try:
            # Make the request to the OpenWeather API
            source = urllib.request.urlopen(url).read()
            list_of_data = json.loads(source)

            data = {
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
                "temp": str(list_of_data['main']['temp']) + ' °C',
                "pressure": str(list_of_data['main']['pressure']),
                "humidity": str(list_of_data['main']['humidity']),
                'main': str(list_of_data['weather'][0]['main']),
                'description': str(list_of_data['weather'][0]['description']),
                'icon': list_of_data['weather'][0]['icon'],
            }

            return render(request, "main/index.html", data)

        except Exception as e:
            print(e)
            return render(request, 'main/index.html', {'error': 'Failed to retrieve weather data.'})
    else:
        return render(request, 'main/index.html', {'error': 'City not provided.'})
