<h1 align="center">Всем здравствуйте, мы команда IGKA</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
<h2 align="center">Наш проект по кейсу media wise</h2>
<h2>Чтобы запустить локально, то просто клонируйте или скачайте наш проект, и запустите сервер через консоль командой python app.py</h2>
<p>также необходимо подгрузить все зависимости через pip install -r requirements.txt</p>
<p> В случае того если возникает ошибка - не хватает модуля (тестили с разных устройств - такое бывает), 
то установить их через команду pip install <название модуля> </p>
<p> Также в файле app.py, могут возникнуть ошибки с доступом папки, если вы тестируте на MACOS, то замените строку с ошибкой на 
from flask import Flask, request, render_template, jsonify, session
from neyron.findbest import predict_best_points  # Импортируем функцию </p>
<h2 align="center">Либо просто перейдите по нашей ссылке!</h2>
<h2 align="center"><a href="https://igka.tech">igka.tech</a></h2>
<h3>С использованием html, css, Java script, Python, Flask и GradientBoostingRegressor, мы смогли реализовать поставленную задачу</h3>
<h3>В веб-интерфейсе есть поля для ввода возраста</h3>
<h4>Первое поля будет началом, а второе концом. То есть От и До</h4>
<h3>Далее есть выбор пола</h3>
<h4>Выбор осуществляется из категорий: Мужчины, Женщины, Мужчины и Женщины</h4>
<h3>Пользователь может ввести нужное количество билбордов, все они образятся на карте</h3>
<h3>Так же выбор доходности населения a, b, c<h3/>
<h4>Можно выбирать любые комбинации, например - ac, ab, b, abc
<h3>Самое крутое, что карта поделена на районы Москвы, и пользователь может выбрать любой район, в котором хочет разместить билборды!</h3>
<h3>Снизу выводится консоль с нужной для пользователя статистикой</h3>
<h4>Выводятся билборды с их координатами, информацией возраста, пола, доходом и нашим предсказанным показателем эффектиности!</h4>
<h3>Если хотите тестировать нейронку и тд, то трогайте только папку neyron. Допусти в ней есть файл find best(def predict_best_points), который прогнозирует лучшие билборды.
modelka.py - обучение модели, procesing.py</h3>
