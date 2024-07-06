import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import re
from sklearn.neighbors import NearestNeighbors

# Загрузим данные из train_data.json
with open('train_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Преобразуем данные в DataFrame
df = pd.json_normalize(data)

# Функция для форматирования поля name
def format_name(name):
    # Извлекаем возрастные параметры из поля name
    parts = name.split()
    if len(parts) >= 2:
        age_from = int(parts[1].split('-')[0])
        age_to = int(parts[1].split('-')[1])
    else:
        age_from = int(parts[0].split('-')[0].replace('All', ''))
        age_to = 60  # По умолчанию, если нет "-" в строке name
    
    return age_from, age_to

# Функция для поиска лучших точек на основе заданных критериев пользователя
def find_best_points(gender, age_from, age_to, num_points):
    # Фильтрация данных по заданным критериям
    filtered_data = df[(df['targetAudience.gender'] == gender) &
                       (df['targetAudience.ageFrom'] == age_from) &
                       (df['targetAudience.ageTo'] == age_to)]
    
    # Применение форматирования к полю name
    filtered_data['targetAudience.ageFrom'], filtered_data['targetAudience.ageTo'] = zip(*filtered_data['targetAudience.name'].map(format_name))
    
    # Выбор только нужных столбцов и преобразование к типу float
    points_data = filtered_data['points'].apply(lambda x: pd.Series(x)).astype(float)
    
    # Подготовка данных для предсказания
    X = points_data.values
    
    # Обучение или загрузка предварительно обученной модели для предсказания value
    # Здесь предполагается, что модель уже обучена и загружена как model
    
    # Нормализация данных
    scaler = StandardScaler()
    scaler.fit(X)
    X_scaled = scaler.transform(X)
    
    # Поиск ближайших соседей
    nbrs = NearestNeighbors(n_neighbors=num_points, algorithm='ball_tree').fit(X_scaled)
    
    # Данные пользователя для предсказания
    user_data = np.array([[gender, age_from, age_to, num_points]])
    user_data_scaled = scaler.transform(user_data)
    
    # Поиск ближайших соседей для данных пользователя
    distances, indices = nbrs.kneighbors(user_data_scaled)
    
    # Вывод лучших точек
    best_points = points_data.iloc[indices[0]]
    
    return best_points