import pandas as pd
import numpy as np
import joblib
import json
from .prop import fileforkolya  # Импорт функции fileforkolya

# Загрузка обученной модели и нормализатора
model = joblib.load('best_gb_model.pkl')
scaler = joblib.load('scaler.pkl')

# Загрузка данных
df = pd.read_csv('formatted_data.csv')

def predict_best_points(gender, age_from, age_to, income, num_points, zona=""):
    # Если zona не пустая, вызываем fileforkolya для создания filtered_data.json
    if zona:
        fileforkolya(zona)
        # Загружаем данные из filtered_data.json
        with open('neyron/filtered_data.json', 'r') as f:
            filtered_data = json.load(f)
        data = pd.DataFrame(filtered_data)
    else:
        # Подготовка данных для предсказания
        data = df[['lat', 'lon', 'azimuth']].drop_duplicates()
        data['gender'] = gender
        data['age_from'] = age_from
        data['age_to'] = age_to
        data['income'] = income
    
    # Преобразование категориальных признаков в числовые
    data = pd.get_dummies(data, columns=['gender', 'income'])
    
    # Заполнение пропущенных колонок dummy значениями
    for col in model.feature_names_in_:
        if col not in data.columns:
            data[col] = 0

    # Предсказание охвата для каждой точки
    data['predicted_value'] = model.predict(data[model.feature_names_in_])
    
    # Денормализация предсказаний
    data['predicted_value'] = scaler.inverse_transform(data['predicted_value'].values.reshape(-1, 1)).flatten()
    
    # Ограничение предсказанных значений
    data['predicted_value'] = data['predicted_value'].clip(0, 100)
    
    # Сортировка точек по предсказанному охвату и выбор лучших
    best_points = data.sort_values(by='predicted_value', ascending=False).head(num_points)

    with open('static/input_data/coordinates.txt', 'w') as f:
        for index, row in best_points.iterrows():
            f.write(f"{row['lat']},{row['lon']}\n")
    return best_points[['lat', 'lon', 'azimuth', 'predicted_value']]

if __name__ == "__main__":
    # Пример использования функции
    gender = 'all'
    age_from = 30
    age_to = 50
    income = 'abc'
    num_points = 5
    zona = "район Бирюлёво Западное"


    best_points = predict_best_points(gender, age_from, age_to, income, num_points, zona)
    print("Best points for the given parameters:")
    print(best_points)