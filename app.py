from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    age_from = int(request.form.get('age-from'))
    age_to = int(request.form.get('age-to'))
    buildboard_number = int(request.form.get('buildboard'))

    if age_from < 18 or age_from > 80 or age_to < 18 or age_to > 80:
        return "Возраст должен быть в диапазоне от 18 до 80 лет", 400

    if buildboard_number < 1 or buildboard_number > 10:
        return "Количество билбордов должно быть от 1 до 10", 400

    # Дополнительная логика обработки данных
    # Например, запись в базу данных или расчёты

    return redirect(url_for('home'))  # Перенаправление на главную страницу после обработки

if __name__ == '__main__':
    app.run(debug=True)
