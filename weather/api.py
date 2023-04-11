import requests, traceback
from datetime import datetime, timedelta
from flask import Blueprint, request, current_app, jsonify

blueprint = Blueprint('api', __name__, url_prefix='/api')

@blueprint.route('/get_weather', methods=['GET'])
def get_weather():
    # Get the city from the query parameters
    city = request.args.get('city')
    api_key = current_app.config['API_KEY']
    units = request.args.get('units').lower()
    
    all_units = {
        'metric' : {
            'temp':'°C',
            'wind' : 'm/s'
        },
        'imperial' : {
            'temp':'°F',
            'wind' : 'mph'
        }
    }

    is_error = False
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}'
        response = requests.get(url)
        data = response.json()
        
    except Exception as e:
        traceback.print_exc()
        is_error = True
    
    weather = {}
    if is_error == False and 'cod' in data and data['cod'] == 200:
        # Extract the relevant weather data from the response
        format_date = datetime.fromtimestamp(data['dt'])
        weather = {
            'city': data['name'],
            'description': data['weather'][0]['description'],
            'temperature': f"{round(data['main']['temp'])}{all_units[units]['temp']}",
            'humidity': data['main']['humidity'],
            'wind_speed': f"{data['wind']['speed']} {all_units[units]['wind']}",
            'date' : format_date.strftime("%Y-%m-%d"),
            'time' : format_date.strftime("%I:%M %p"),
            'icon' : f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
        }

    # Return the weather data as a JSON response
    return jsonify(weather)

@blueprint.route('/get_weather_forcast', methods=['GET'])
def get_weather_forcast():

    city = request.args.get('city')
    api_key = current_app.config['API_KEY']
    units = request.args.get('units')
    weather = {}
    all_units = {
        'metric' : {
            'temp':'°C',
            'wind' : 'm/s'
        },
        'imperial' : {
            'temp':'°F',
            'wind' : 'mph'
        }
    }

    is_error = False
    try:
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}'
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        traceback.print_exc()
        is_error = True

    if is_error == False and 'cod' in data and data['cod'] == '200':
        weather_data = []
        for result in data['list']:
            format_date = datetime.fromtimestamp(result['dt'])
            weather_data.append({
                'date' : format_date.strftime("%Y-%m-%d"),
                'time' : format_date.strftime("%I:%M %p"),
                'description': result['weather'][0]['description'],
                'temperature': f"{round(result['main']['temp'])}{all_units[units]['temp']}",
                'humidity': result['main']['humidity'],
                'wind_speed': f"{result['wind']['speed']} {all_units[units]['wind']}",
                'icon' : f"https://openweathermap.org/img/wn/{result['weather'][0]['icon']}@2x.png",
            })

        # start_date = datetime.utcnow()
        # end_date = start_date + timedelta(days=5)

        current_date_utc = datetime.utcnow()
        current_date = current_date_utc.strftime("%Y-%m-%d")
        start_date = datetime.strptime(weather_data[0]['date'], "%Y-%m-%d")
        end_date = datetime.strptime(weather_data[-1]['date'], "%Y-%m-%d")
        step = timedelta(days = 1)

        date_array = []
        while start_date <= end_date:
            date_array.append(start_date.strftime("%Y-%m-%d"))
            start_date += step

        inc = 0
        final_array = []
        while inc < len(date_array):
            temp_data = []
            for d in weather_data:
                if date_array[inc] == d['date']:
                    temp_data.append(d)
            final_array.append({date_array[inc] : temp_data})
            inc += 1

        # Extract the relevant weather data from the response
        weather = {
            'city': data['city']['name'],
            'data' : final_array
        }

    # Return the weather data as a JSON response
    return jsonify(weather)