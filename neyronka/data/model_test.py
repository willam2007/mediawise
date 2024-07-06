import joblib
import pandas as pd

# Загрузка сохраненной модели
model_path = 'neyronka/models/linear_regression_model.pkl'
model = joblib.load(model_path)

# Пример данных для предсказания (можете заменить на свои данные)
data_to_predict = pd.DataFrame({
    'ageFrom': [30, 25],
    'ageTo': [45, 35],
    'lat': [55.5, 56.0],
    'lon': [37.6, 37.7],
    'azimuth': [270, 180]
})

# Предсказание с помощью загруженной модели
predictions = model.predict(data_to_predict)

# Вывод предсказанных значений
for i, pred in enumerate(predictions):
    print(f'Prediction {i+1}: {pred}')