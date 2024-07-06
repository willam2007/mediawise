import pandas as pd
import json
from sklearn.preprocessing import LabelEncoder, StandardScaler


# Загрузка данных
with open('neyronka/data/train_data.json', 'r') as f:
    data = json.load(f)

# Преобразование данных в DataFrame
def preprocess_data(data):
    records = []
    for record in data:
        audience = record['targetAudience']
        points = record['points']
        value = record['value']
        
        for point in points:
            records.append({
                'hash': record['hash'],
                'name': audience['name'],
                'gender': audience['gender'],
                'ageFrom': audience['ageFrom'],
                'ageTo': audience['ageTo'],
                'income': audience['income'],
                'lat': point['lat'],
                'lon': point['lon'],
                'azimuth': point['azimuth'],
                'value': value
            })
    
    df = pd.DataFrame(records)
    return df

df = preprocess_data(data)

# Кодирование категориальных переменных
le_gender = LabelEncoder()
df['gender'] = le_gender.fit_transform(df['gender'])

le_income = LabelEncoder()
df['income'] = le_income.fit_transform(df['income'])

# Нормализация числовых переменных
scaler = StandardScaler()
df[['ageFrom', 'ageTo', 'lat', 'lon', 'azimuth']] = scaler.fit_transform(df[['ageFrom', 'ageTo', 'lat', 'lon', 'azimuth']])

# Сохранение обработанных данных
df.to_csv('neyronka/data/processed_data.csv', index=False)

# Проверка данных
print(df.head())