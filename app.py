import sys
from flask import Flask, request, render_template, redirect, url_for, jsonify
import subprocess
import os
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
    buildboard_number = int(request.form.get('buildboard'))
    gender = request.form.get('SexStatus')  # Получаем выбранный пол
    # Получаем выбранные варианты чекбокса
    selected_options = request.form.getlist('options')
    print("Выбранные варианты:", selected_options)


    # Проверка диапазона возраста
    if age_from < 18 or age_from > 80 or age_to < 18 or age_to > 80:
        return "Возраст должен быть в диапазоне от 18 до 80 лет", 400

    # Проверка количества билбордов
    if buildboard_number < 1 or buildboard_number > 10:
        return "Количество билбордов должно быть от 1 до 10", 400
    district_name = ""

    predict_best_points(gender,age_from, age_to,selected_options,buildboard_number,district_name)
    # Перенаправление на главную страницу после успешной обработки данных
    return redirect(url_for('home'))

@app.route('/set-district', methods=['POST'])
def set_district():
    # Получение названия района из запроса
    district_name = ""
    district_name = request.json['districtName'] 
    print(f"Получено название района: {district_name}")
    
    # Сохранение названия района
    save_district_name(district_name)
    
    # Отправка ответа о успехе
    return jsonify({'status': 'success', 'districtName': district_name})

def save_district_name(district_name):
    # Запись названия района в файл
    with open('./static/district_choise/district_name.txt', 'w') as file:
        file.write(district_name)
    
    # Запуск внешнего скрипта Python после сохранения названия района
    run_district_change_script()

def run_district_change_script():
    # Вызов скрипта district_change.py и вывод результатов его работы
    result = subprocess.run(['python', './static/district_choise/district_change.py'], capture_output=True, text=True)
    if result.returncode == 0:
        print("Скрипт выполнен успешно")
    else:
        print(f"Ошибка выполнения скрипта: {result.stderr}")

# Запуск приложения Flask
if __name__ == '__main__':
    app.run(debug=True)
