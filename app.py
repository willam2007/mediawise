
import sys
from flask import Flask, request, render_template, redirect, url_for, jsonify
import subprocess
import os
import logging

# Добавляем путь к папке neyron
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'neyron')))
# Теперь можно импортировать функцию
from findbest import predict_best_points




# Создаем экземпляр Flask-приложения
app = Flask(__name__)

@app.route('/')
def home():
    # Отображение главной страницы
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Получаем данные из формы
    age_from = int(request.form.get('age-from'))
    age_to = int(request.form.get('age-to'))
    sex_status = request.form.get('SexStatus')
    buildboard_number = int(request.form.get('buildboard'))
    # Получаем выбранные варианты чекбокса
    selected_options = request.form.getlist('options')
    selected_options_str = ''.join(selected_options)
    selected_district = ""
    selected_district = request.form.get('selectedDistrict')

    print(f"Возраст от: {age_from}, до: {age_to}")
    print(f"Пол: {sex_status}")
    print(f"Количество билбордов: {buildboard_number}")
    print(f"Выбранные варианты: {selected_options}")
    print(f"Выбранный район: {selected_district}")

    # Проверка диапазона возраста
    if age_from < 18 or age_from > 80 or age_to < 18 or age_to > 80:
        return "Возраст должен быть в диапазоне от 18 до 80 лет", 400

    # Проверка количества билбордов
    if buildboard_number < 1 or buildboard_number > 50:
        return "Количество билбордов должно быть от 1 до 10", 400

    # Вызов функции для генерации лучших точек
    best_points = predict_best_points(sex_status, age_from, age_to, selected_options_str, buildboard_number, selected_district)
    print(f"Лучшие точки: {best_points}")

    # Перенаправление на главную страницу после успешной обработки данных
    return redirect(url_for('home'))

    

# Запуск приложения Flask
if __name__ == '__main__':
    app.run(debug=True) 