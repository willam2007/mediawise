
import sys
from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import subprocess
import os
import logging

# Добавляем путь к папке neyron
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'neyron')))
# Теперь можно импортировать функцию
from findbest import predict_best_points




# Создаем экземпляр Flask-приложения
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Секретный ключ для сессий

@app.route('/')
def home():
    response_data = session.pop('response_data', None)
    return render_template('index.html', response_data=response_data)

@app.route('/submit', methods=['POST'])
def submit():
    age_from = int(request.form.get('age-from'))
    age_to = int(request.form.get('age-to'))
    sex_status = request.form.get('SexStatus')
    buildboard_number = int(request.form.get('buildboard'))
    selected_options = request.form.getlist('options')
    selected_options_str = ''.join(selected_options)
    selected_district = request.form.get('selectedDistrict')
    if selected_district == 'null':
        selected_district = ''

    print(f"Возраст от: {age_from}, до: {age_to}")
    print(f"Пол: {sex_status}")
    print(f"Количество билбордов: {buildboard_number}")
    print(f"Выбранные варианты: {selected_options}")
    print(f"Выбранный район: {selected_district}")

    if age_from < 18 or age_from > 80 or age_to < 18 or age_to > 80:
        return "Возраст должен быть в диапазоне от 18 до 80 лет", 400

    if buildboard_number < 1 or buildboard_number > 50:
        return "Количество билбордов должно быть от 1 до 10", 400

    best_points = predict_best_points(sex_status, age_from, age_to, selected_options_str, buildboard_number, selected_district)
    best_points_list = best_points.to_dict(orient='records')

    response_data = {
        'age_from': age_from,
        'age_to': age_to,
        'sex_status': sex_status,
        'buildboard_number': buildboard_number,
        'selected_options': selected_options,
        'selected_district': selected_district,
        'best_points': best_points_list
    }

    session['response_data'] = response_data

    return jsonify(response_data)

@app.route('/clear-coordinates', methods=['POST'])
def clear_coordinates():
    clear_coordinates_file()
    return '', 204  # Возвращаем успешный статус без содержания

def clear_coordinates_file():
    with open('./static/input_data/coordinates.txt', 'w') as file:
        file.write('')

if __name__ == '__main__':
    clear_coordinates_file()
    app.run(debug=True)
