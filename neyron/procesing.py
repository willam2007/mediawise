import pandas as pd
import json

# Чтение данных из JSON файла
with open('neyron/train_data.json', 'r') as file:
    data = json.load(file)

# Функция для извлечения данных из одной записи
def extract_data(record):
    hash_value = record['hash']
    target_audience = record['targetAudience']
    gender = target_audience['gender']
    age_from = target_audience['ageFrom']
    age_to = target_audience['ageTo']
    income = target_audience['income']
    points = record['points']
    value = record['value']
    
    # Создаем список данных для каждой точки
    point_data = []
    for point in points:
        lat = point['lat']
        lon = point['lon']
        azimuth = point['azimuth']
        point_data.append([hash_value, gender, age_from, age_to, income, lat, lon, azimuth, value])
    
    return point_data

# Извлечение данных из всех записей
all_data = []
for record in data:
    all_data.extend(extract_data(record))

# Создание DataFrame
columns = ['hash', 'gender', 'age_from', 'age_to', 'income', 'lat', 'lon', 'azimuth', 'value']
df = pd.DataFrame(all_data, columns=columns)

# Сохранение DataFrame в файл CSV
df.to_csv('formatted_data.csv', index=False)

print(df.head())