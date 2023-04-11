import traceback, requests
from flask import Blueprint, flash, g, redirect, render_template, request, url_for, current_app, jsonify
from werkzeug.exceptions import abort

from weather.db import get_db
from weather.auth import login_required

blueprint = Blueprint('main', __name__)

@blueprint.route('/',methods=('GET', 'POST'))
@login_required
def index():

    weather_data = []
    if request.method == 'POST':
        city = request.form['city']
        temp_units = request.form['temp_units']
        weather_data = {}

        try:
            url = f"{current_app.config['BASE_URL']}/api/get_weather?city={city}&units={temp_units}"
            response = requests.get(url)
            weather_data = response.json()
        except Exception as e:
            traceback.print_exc()

    return render_template('weather/index.html', weather_data=weather_data)

@blueprint.route('/forcast',methods=('GET', 'POST'))
@login_required
def forcast():
    weather_data = []
    if request.method == 'POST':
        city = request.form['city']
        temp_units = request.form['temp_units']
        weather_data = {}

        try:
            url = f"{current_app.config['BASE_URL']}/api/get_weather_forcast?city={city}&units={temp_units}"
            response = requests.get(url)
            weather_data = response.json()
        except Exception as e:
            traceback.print_exc()

    return render_template('weather/forcast.html', weather_data=weather_data)